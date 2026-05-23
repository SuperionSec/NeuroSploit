"""
NeuroSploit v3 - Validation Judge

Sole authority for approving or rejecting vulnerability findings.
No finding enters the confirmed list without passing through this judge.

Pipeline:
    1. Run negative controls (benign payloads → compare responses)
    2. Check proof of execution (per vuln type)
    3. Get AI interpretation (BEFORE verdict, not after)
    4. Calculate confidence score (0-100)
    5. Apply verdict (confirmed/likely/rejected)
"""

import logging
from dataclasses import dataclass, field, asdict
from typing import Callable, Dict, List, Optional, Any

from app.core.neurosploit.negative_control import NegativeControlEngine, NegativeControlResult
from app.core.neurosploit.proof_of_execution import ProofOfExecution, ProofResult
from app.core.neurosploit.confidence_scorer import ConfidenceScorer, ConfidenceResult

logger = logging.getLogger(__name__)


@dataclass
class JudgmentResult:
    """Complete judgment result from the ValidationJudge."""
    approved: bool
    verdict: str
    confidence_score: int
    confidence_breakdown: Dict[str, int] = field(default_factory=dict)
    proof_of_execution: Optional[ProofResult] = None
    negative_controls: Optional[NegativeControlResult] = None
    ai_interpretation: Optional[str] = None
    evidence_summary: str = ""
    rejection_reason: str = ""


class ValidationJudge:
    """Sole authority for approving/rejecting vulnerability findings.

    Orchestrates negative controls, proof of execution, AI interpretation,
    and confidence scoring into a single JudgmentResult.

    Usage:
        judge = ValidationJudge(controls, proof, scorer, llm)
        judgment = await judge.evaluate(
            vuln_type, url, param, payload, test_response, baseline,
            signals, evidence, make_request_fn
        )
        if judgment.approved:
            # Create finding with judgment.confidence_score
        else:
            # Store as rejected finding with judgment.rejection_reason
    """

    def __init__(
        self,
        negative_controls: NegativeControlEngine,
        proof_engine: ProofOfExecution,
        confidence_scorer: ConfidenceScorer,
        llm: Any = None,
        access_control_learner: Any = None,
        methodology_index: Any = None,
    ):
        self.controls = negative_controls
        self.proof = proof_engine
        self.scorer = confidence_scorer
        self.llm = llm
        self.acl_learner = access_control_learner
        self.methodology_index = methodology_index

    async def evaluate(
        self,
        vuln_type: str,
        url: str,
        param: str,
        payload: str,
        test_response: Dict,
        baseline: Optional[Dict],
        signals: List[str],
        evidence: str,
        make_request_fn: Callable,
        method: str = "GET",
        injection_point: str = "parameter",
    ) -> JudgmentResult:
        """Full evaluation pipeline.

        Args:
            vuln_type: Vulnerability type (e.g., "ssrf", "xss_reflected")
            url: Target URL
            param: Parameter being tested
            payload: The attack payload used
            test_response: HTTP response dict from the attack
            baseline: Optional baseline response for comparison
            signals: Signal names from multi_signal_verify (e.g., ["baseline_diff"])
            evidence: Raw evidence string from verification
            make_request_fn: Async fn(url, method, params) → response dict
            method: HTTP method used
            injection_point: Where payload was injected

        Returns:
            JudgmentResult with verdict, score, proof, controls, evidence
        """
        control_result = await self._run_controls(
            url, param, method, vuln_type, test_response,
            make_request_fn, baseline, injection_point
        )

        proof_result = self.proof.check(
            vuln_type, payload, test_response, baseline
        )

        ai_interp = await self._get_ai_interpretation(
            vuln_type, payload, test_response
        )

        confidence = self.scorer.calculate(
            signals, proof_result, control_result, ai_interp
        )

        if self.acl_learner:
            try:
                body = test_response.get("body", "") if isinstance(test_response, dict) else ""
                status = test_response.get("status", 0) if isinstance(test_response, dict) else 0
                hints = self.acl_learner.get_evaluation_hints(vuln_type, body, status)
                if hints and hints.get("likely_false_positive") and hints.get("fp_signals", 0) >= 2:
                    fp_rate = self.acl_learner.get_false_positive_rate(vuln_type)
                    if fp_rate > 0.7:
                        penalty = -20
                        confidence.score = max(0, confidence.score + penalty)
                        confidence.breakdown["acl_learning_penalty"] = penalty
                        confidence.detail += f"; ACL learning penalty ({penalty}pts, FP rate: {fp_rate:.0%})"
                        if confidence.score >= self.scorer.THRESHOLD_CONFIRMED:
                            confidence.verdict = "confirmed"
                        elif confidence.score >= self.scorer.THRESHOLD_LIKELY:
                            confidence.verdict = "likely"
                        else:
                            confidence.verdict = "rejected"
            except Exception:
                pass

        approved = confidence.verdict != "rejected"

        evidence_summary = self._build_evidence_summary(
            evidence, proof_result, control_result, confidence, ai_interp
        )

        rejection_reason = ""
        if not approved:
            rejection_reason = self._build_rejection_reason(
                vuln_type, param, proof_result, control_result,
                confidence, ai_interp
            )

        return JudgmentResult(
            approved=approved,
            verdict=confidence.verdict,
            confidence_score=confidence.score,
            confidence_breakdown=confidence.breakdown,
            proof_of_execution=proof_result,
            negative_controls=control_result,
            ai_interpretation=ai_interp,
            evidence_summary=evidence_summary,
            rejection_reason=rejection_reason,
        )

    async def _run_controls(
        self,
        url: str,
        param: str,
        method: str,
        vuln_type: str,
        attack_response: Dict,
        make_request_fn: Callable,
        baseline: Optional[Dict],
        injection_point: str,
    ) -> Optional[NegativeControlResult]:
        """Run negative controls with error handling."""
        try:
            return await self.controls.run_controls(
                url, param, method, vuln_type, attack_response,
                make_request_fn, baseline, injection_point
            )
        except Exception as e:
            logger.debug(f"Negative controls failed: {e}")
            return None

    async def _get_ai_interpretation(
        self,
        vuln_type: str,
        payload: str,
        response: Dict,
    ) -> Optional[str]:
        """Get AI interpretation of the response (BEFORE verdict)."""
        if not self.llm or not self.llm.is_available():
            return None

        try:
            body = response.get("body", "")[:1000]
            status = response.get("status", 0)

            acl_hint = ""
            if self.acl_learner:
                hints = self.acl_learner.get_evaluation_hints(vuln_type, body, status)
                if hints and hints.get("matching_patterns", 0) > 0:
                    fp_label = "LIKELY FALSE POSITIVE" if hints["likely_false_positive"] else "POSSIBLY REAL"
                    acl_hint = (
                        f"\n\n**Learned Pattern Hints:** {fp_label} "
                        f"(pattern: {hints['pattern_type']}, "
                        f"FP signals: {hints['fp_signals']}, TP signals: {hints['tp_signals']})\n"
                        f"IMPORTANT: For access control vulns (BOLA/BFLA/IDOR), do NOT rely on "
                        f"HTTP status codes. Compare actual response DATA — check if different "
                        f"user's private data is returned vs. denial/empty/own-data patterns."
                    )

            prompt = f"""Briefly analyze this HTTP response after testing for {vuln_type.upper()}.

Payload sent: {payload[:200]}
Response status: {status}

Response excerpt:
```
{body}
```
{acl_hint}

Answer in 1-2 sentences: Was the payload processed/executed? Or was it ignored/filtered/blocked? Be specific about what happened."""

            system = self._get_prompt_for_vuln_type(vuln_type, "interpretation")
            if self.methodology_index:
                extra = self.methodology_index.get_for_vuln_and_context(
                    vuln_type, "interpretation", max_chars=1000)
                if extra:
                    system += f"\n\n## EXTERNAL METHODOLOGY\n{extra}"
            result = await self.llm.generate(prompt, system)
            return result.strip()[:300] if result else None
        except Exception:
            return None

    def _get_prompt_for_vuln_type(self, vuln_type: str, context: str = "interpretation") -> str:
        """Get system prompt for a vulnerability type.

        Uses graceful degradation if vuln_engine prompts are not available.
        """
        try:
            from app.core.neurosploit.vuln_engine.system_prompts import get_prompt_for_vuln_type as _get_prompt
            return _get_prompt(vuln_type, context)
        except ImportError:
            return "You are a security analysis assistant. Be concise and technical."

    def _build_evidence_summary(
        self,
        raw_evidence: str,
        proof: Optional[ProofResult],
        controls: Optional[NegativeControlResult],
        confidence: ConfidenceResult,
        ai_interp: Optional[str],
    ) -> str:
        """Build hardened evidence string with all verification components."""
        parts = []

        if raw_evidence:
            parts.append(raw_evidence)

        if proof:
            if proof.proven:
                parts.append(f"[PROOF] {proof.proof_type}: {proof.detail}")
            else:
                parts.append(f"[NO PROOF] {proof.detail}")

        if controls:
            parts.append(f"[CONTROLS] {controls.detail}")

        if ai_interp:
            parts.append(f"[AI] {ai_interp}")

        parts.append(f"[CONFIDENCE] {confidence.score}/100 [{confidence.verdict}]")

        return " | ".join(parts)

    def _build_rejection_reason(
        self,
        vuln_type: str,
        param: str,
        proof: Optional[ProofResult],
        controls: Optional[NegativeControlResult],
        confidence: ConfidenceResult,
        ai_interp: Optional[str],
    ) -> str:
        """Build clear rejection reason explaining why finding was rejected."""
        reasons = []

        if proof and not proof.proven:
            reasons.append("no proof of execution")

        if controls and controls.same_behavior:
            reasons.append(
                f"negative controls show same behavior "
                f"({controls.controls_matching}/{controls.controls_run} controls match)"
            )

        if ai_interp:
            ineffective_kws = ["ignored", "not processed", "blocked", "filtered",
                              "sanitized", "no effect"]
            if any(kw in ai_interp.lower() for kw in ineffective_kws):
                reasons.append(f"AI confirms payload was ineffective")

        reason_str = "; ".join(reasons) if reasons else "confidence too low"

        return (f"Rejected {vuln_type} in {param}: {reason_str} "
                f"(score: {confidence.score}/100)")