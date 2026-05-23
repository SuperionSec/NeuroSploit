import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set
from urllib.parse import urlparse

from app.core.neurosploit.vuln_engine.registry import VulnerabilityRegistry, VulnTypeInfo
from app.core.neurosploit.vuln_engine.payload_generator import PayloadGenerator
from app.core.neurosploit.vuln_engine.ai_prompts import AIVulnPromptBuilder
from app.core.neurosploit.vuln_engine.pentest_playbook import PentestPlaybook
from app.core.neurosploit.request_engine import RequestEngine, RequestResult, ErrorType
from app.core.neurosploit.proof_of_execution import ProofOfExecution, ProofResult
from app.core.neurosploit.negative_control import NegativeControlEngine, NegativeControlResult
from app.core.neurosploit.confidence_scorer import ConfidenceScorer, ConfidenceResult
from app.core.neurosploit.validation_judge import ValidationJudge, Verdict
from app.core.neurosploit.response_verifier import ResponseVerifier
from app.core.neurosploit.llm_manager import LLMManager
from app.core.neurosploit.waf_detector import WAFDetector

logger = logging.getLogger(__name__)


@dataclass
class Finding:
    vuln_type: str
    url: str
    param: str
    severity: str
    confidence_score: int
    proof_type: str
    evidence: str
    request_details: Dict[str, Any] = field(default_factory=dict)
    response_details: Dict[str, Any] = field(default_factory=dict)
    remediation: str = ""
    ai_analysis: str = ""
    timestamp: float = 0.0
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vuln_type": self.vuln_type,
            "url": self.url,
            "param": self.param,
            "severity": self.severity,
            "confidence_score": self.confidence_score,
            "proof_type": self.proof_type,
            "evidence": self.evidence,
            "request_details": self.request_details,
            "response_details": self.response_details,
            "remediation": self.remediation,
            "ai_analysis": self.ai_analysis,
            "timestamp": self.timestamp,
            "tags": self.tags,
        }


@dataclass
class ScanResult:
    target_url: str
    vuln_types_tested: List[str]
    findings: List[Finding]
    total_requests: int
    duration: float
    stats: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_url": self.target_url,
            "vuln_types_tested": self.vuln_types_tested,
            "findings": [f.to_dict() for f in self.findings],
            "total_requests": self.total_requests,
            "duration": round(self.duration, 2),
            "stats": self.stats,
        }


class VulnEngine:

    def __init__(
        self,
        request_engine: RequestEngine,
        llm_manager: Optional[LLMManager] = None,
        registry: Optional[VulnerabilityRegistry] = None,
        max_concurrent: int = 10,
        is_cancelled_fn: Optional[Callable] = None,
    ):
        self.request_engine = request_engine
        self.llm = llm_manager
        self.registry = registry or VulnerabilityRegistry()
        self.max_concurrent = max_concurrent
        self.is_cancelled = is_cancelled_fn or (lambda: False)
        self.payload_gen = PayloadGenerator()
        self.prompt_builder = AIVulnPromptBuilder()
        self.playbook = PentestPlaybook()
        self.proof_checker = ProofOfExecution()
        self.neg_control = NegativeControlEngine()
        self.confidence_scorer = ConfidenceScorer()
        self.judge = ValidationJudge()
        self.verifier = ResponseVerifier()
        self.waf_detector = WAFDetector(request_engine)
        self._findings: List[Finding] = []
        self._tested_params: Set[str] = set()

    async def scan(
        self,
        target_url: str,
        vuln_types: Optional[List[str]] = None,
        params: Optional[List[str]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
    ) -> ScanResult:
        start_time = time.monotonic()
        if not vuln_types:
            vuln_types = self.registry.all_keys()
        if not params:
            params = await self._discover_params(target_url)
        parsed = urlparse(target_url)
        base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        all_findings: List[Finding] = []
        batch_size = self.max_concurrent
        vuln_batches = [vuln_types[i:i+batch_size] for i in range(0, len(vuln_types), batch_size)]
        for batch in vuln_batches:
            if self.is_cancelled():
                break
            tasks = []
            for vt in batch:
                for param in (params or ["test"]):
                    task = asyncio.create_task(self._test_vuln(target_url, vt, param, headers, cookies))
                    tasks.append(task)
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for r in results:
                if isinstance(r, Finding):
                    all_findings.append(r)
                elif isinstance(r, Exception):
                    logger.error(f"VulnEngine scan error: {r}")
        self._findings.extend(all_findings)
        duration = time.monotonic() - start_time
        return ScanResult(
            target_url=target_url,
            vuln_types_tested=vuln_types,
            findings=all_findings,
            total_requests=self.request_engine.total_requests,
            duration=duration,
            stats=self._build_stats(all_findings),
        )

    async def _test_vuln(
        self,
        url: str,
        vuln_type: str,
        param: str,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
    ) -> Optional[Finding]:
        if self.is_cancelled():
            return None
        vuln_info = self.registry.get(vuln_type)
        if not vuln_info:
            return None
        payloads = self.payload_gen.generate_for_type(vuln_type, limit=5)
        if not payloads:
            return None
        waf_result = await self.waf_detector.detect(url)
        if waf_result.detected_wafs:
            payloads = self.waf_detector.adapt_payload_set(payloads, waf_result, vuln_type=vuln_type)
        for payload in payloads:
            if self.is_cancelled():
                return None
            resp = await self.request_engine.request(
                url, method="GET", params={param: payload},
                headers=headers, cookies=cookies,
            )
            if not resp or resp.error_type != ErrorType.SUCCESS:
                continue
            signals = self.verifier.verify(resp, payload, vuln_type)
            proof_result = await self.proof_checker.check(
                vuln_type, resp, payload, url, self.llm
            )
            if not proof_result or not proof_result.proven:
                continue
            control_result = await self.neg_control.run_controls(
                url, param, "GET", vuln_type,
                {"status": resp.status, "body": resp.body, "headers": resp.headers},
                lambda u, m, p: self._make_control_request(u, m, p, headers, cookies),
            )
            ai_interpretation = ""
            if self.llm:
                ai_prompt = self.prompt_builder.build_decision_prompt(
                    vuln_type, resp.body, payload, signals
                )
                ai_resp = await self.llm.generate(ai_prompt)
                if not ai_resp.is_error:
                    ai_interpretation = ai_resp.content
            confidence = self.confidence_scorer.calculate(
                signals, proof_result, control_result, ai_interpretation
            )
            verdict = self.judge.decide(
                confidence, proof_result, control_result, signals, vuln_type
            )
            if verdict.approved:
                finding = Finding(
                    vuln_type=vuln_type,
                    url=url,
                    param=param,
                    severity=vuln_info.severity,
                    confidence_score=confidence.score,
                    proof_type=proof_result.proof_type,
                    evidence=proof_result.evidence[:500],
                    request_details={"url": url, "param": param, "payload": payload[:200]},
                    response_details={"status": resp.status, "body_preview": resp.body[:500]},
                    remediation=vuln_info.remediation,
                    ai_analysis=ai_interpretation[:500],
                    timestamp=time.time(),
                    tags=self._infer_tags(vuln_type, signals),
                )
                return finding
        return None

    async def _make_control_request(
        self, url: str, method: str, params: Dict,
        headers: Optional[Dict], cookies: Optional[Dict],
    ) -> Optional[Dict]:
        resp = await self.request_engine.request(url, method=method, params=params, headers=headers, cookies=cookies)
        if resp:
            return {"status": resp.status, "body": resp.body, "headers": resp.headers}
        return None

    async def _discover_params(self, url: str) -> List[str]:
        parsed = urlparse(url)
        if parsed.query:
            from urllib.parse import parse_qs
            qs = parse_qs(parsed.query)
            return list(qs.keys())
        return ["q", "search", "id", "page", "input", "name", "value"]

    def _build_stats(self, findings: List[Finding]) -> Dict[str, Any]:
        by_severity = {}
        by_type = {}
        for f in findings:
            by_severity[f.severity] = by_severity.get(f.severity, 0) + 1
            by_type[f.vuln_type] = by_type.get(f.vuln_type, 0) + 1
        return {
            "total_findings": len(findings),
            "by_severity": by_severity,
            "by_type": by_type,
            "avg_confidence": sum(f.confidence_score for f in findings) / max(len(findings), 1),
        }

    def _infer_tags(self, vuln_type: str, signals: List[str]) -> List[str]:
        tags = [vuln_type]
        if "payload_effect" in signals:
            tags.append("payload_reflected")
        if "error_leak" in signals:
            tags.append("error_disclosure")
        if "timing_diff" in signals:
            tags.append("timing_based")
        if "code_execution" in signals:
            tags.append("code_execution")
        return tags

    def get_findings(self) -> List[Finding]:
        return list(self._findings)

    def clear_findings(self):
        self._findings.clear()