"""
NeuroSploit v3 - Negative Control Engine

Sends benign/control payloads and compares responses to detect false positives
from same-behavior patterns. If the application responds the same way to a
benign value as it does to an attack payload, the finding is likely a false positive.
"""

import hashlib
import logging
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple, Any
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

logger = logging.getLogger(__name__)


@dataclass
class ControlTestResult:
    """Result of a single control test."""
    control_type: str
    control_value: str
    status_match: bool
    length_similar: bool
    hash_match: bool
    same_behavior: bool
    detail: str = ""


@dataclass
class NegativeControlResult:
    """Aggregated result of all negative control tests."""
    same_behavior: bool
    controls_run: int
    controls_matching: int
    confidence_adjustment: int
    results: List[ControlTestResult] = field(default_factory=list)
    detail: str = ""


class NegativeControlEngine:
    """Sends control payloads to detect false positives from same-behavior responses.

    The key insight: if the application responds identically to "test123" and
    to "<script>alert(1)</script>", then the XSS payload was NOT processed —
    the application simply ignores or sanitizes the parameter entirely.
    """

    BENIGN_PAYLOADS: Dict[str, List[str]] = {
        "xss_reflected": ["test123", "hello world"],
        "xss_stored": ["test123", "hello world"],
        "xss_dom": ["test123", "hello world"],
        "xss": ["test123", "hello world"],

        "sqli": ["1", "test"],
        "sqli_error": ["1", "test"],
        "sqli_union": ["1", "test"],
        "sqli_blind": ["1", "test"],
        "sqli_time": ["1", "test"],

        "ssrf": ["https://www.example.com", "test"],
        "ssrf_cloud": ["https://www.example.com", "test"],

        "lfi": ["index.html", "test.txt"],
        "path_traversal": ["index.html", "test.txt"],

        "ssti": ["hello", "12345"],

        "rce": ["test", "hello"],
        "command_injection": ["test", "hello"],

        "open_redirect": ["/", "/index.html"],

        "crlf_injection": ["test-value", "normal"],
        "header_injection": ["test-value", "normal"],

        "xxe": ["test", "hello"],

        "nosql_injection": ["test", "1"],

        "host_header_injection": ["localhost", "example.com"],

        "default": ["test123", "benign_value"],
    }

    LENGTH_THRESHOLD_PCT = 5.0

    async def run_controls(
        self,
        url: str,
        param: str,
        method: str,
        vuln_type: str,
        attack_response: Dict,
        make_request_fn: Callable,
        baseline: Optional[Dict] = None,
        injection_point: str = "parameter",
    ) -> NegativeControlResult:
        """Run negative control tests and compare with the attack response.

        Args:
            url: Target URL
            param: Parameter name being tested
            method: HTTP method
            vuln_type: Vulnerability type
            attack_response: The response from the attack payload
            make_request_fn: Async function to make HTTP requests
            baseline: Optional baseline response
            injection_point: Where payload is injected (parameter, header, body, path)

        Returns:
            NegativeControlResult with same_behavior flag and details
        """
        results: List[ControlTestResult] = []
        controls_matching = 0

        attack_status = attack_response.get("status", 0)
        attack_body = attack_response.get("body", "")
        attack_length = len(attack_body)
        attack_hash = hashlib.md5(
            attack_body.encode("utf-8", errors="replace")
        ).hexdigest()

        base_type = vuln_type.split("_")[0] if "_" in vuln_type else vuln_type
        benign_values = self.BENIGN_PAYLOADS.get(
            vuln_type,
            self.BENIGN_PAYLOADS.get(base_type, self.BENIGN_PAYLOADS["default"])
        )

        for benign in benign_values[:2]:
            try:
                control_resp = await self._send_control(
                    url, param, method, benign, make_request_fn, injection_point
                )
                if control_resp:
                    result = self._compare_responses(
                        "benign", benign, attack_status, attack_length,
                        attack_hash, control_resp
                    )
                    results.append(result)
                    if result.same_behavior:
                        controls_matching += 1
            except Exception as e:
                logger.debug(f"Negative control (benign) failed: {e}")

        try:
            control_resp = await self._send_control(
                url, param, method, "", make_request_fn, injection_point
            )
            if control_resp:
                result = self._compare_responses(
                    "empty", "", attack_status, attack_length,
                    attack_hash, control_resp
                )
                results.append(result)
                if result.same_behavior:
                    controls_matching += 1
        except Exception as e:
            logger.debug(f"Negative control (empty) failed: {e}")

        if injection_point == "parameter" and param:
            try:
                control_resp = await self._send_without_param(
                    url, param, method, make_request_fn
                )
                if control_resp:
                    result = self._compare_responses(
                        "no_param", "(omitted)", attack_status, attack_length,
                        attack_hash, control_resp
                    )
                    results.append(result)
                    if result.same_behavior:
                        controls_matching += 1
            except Exception as e:
                logger.debug(f"Negative control (no_param) failed: {e}")

        controls_run = len(results)
        same_behavior = controls_matching > 0

        if same_behavior:
            matching_types = [r.control_type for r in results if r.same_behavior]
            detail = (f"NEGATIVE CONTROL FAILED: {controls_matching}/{controls_run} "
                     f"controls show same behavior as attack ({', '.join(matching_types)})")
        else:
            detail = f"Negative controls passed: 0/{controls_run} controls match attack response"

        return NegativeControlResult(
            same_behavior=same_behavior,
            controls_run=controls_run,
            controls_matching=controls_matching,
            confidence_adjustment=-60 if same_behavior else 20,
            results=results,
            detail=detail,
        )

    async def _send_control(
        self,
        url: str,
        param: str,
        method: str,
        value: str,
        make_request_fn: Callable,
        injection_point: str,
    ) -> Optional[Dict]:
        """Send a control request with the given value."""
        if injection_point == "parameter":
            return await make_request_fn(url, method, {param: value})
        elif injection_point == "header":
            return await make_request_fn(url, method, {param: value})
        elif injection_point == "path":
            parsed = urlparse(url)
            control_url = urlunparse(parsed._replace(
                path=parsed.path.rstrip("/") + "/" + value
            ))
            return await make_request_fn(control_url, method, {})
        elif injection_point == "body":
            return await make_request_fn(url, method, {param: value})
        else:
            return await make_request_fn(url, method, {param: value})

    async def _send_without_param(
        self,
        url: str,
        param: str,
        method: str,
        make_request_fn: Callable,
    ) -> Optional[Dict]:
        """Send request without the tested parameter."""
        parsed = urlparse(url)
        if parsed.query:
            params = parse_qs(parsed.query, keep_blank_values=True)
            params.pop(param, None)
            new_query = urlencode(params, doseq=True)
            clean_url = urlunparse(parsed._replace(query=new_query))
        else:
            clean_url = url

        return await make_request_fn(clean_url, method, {})

    def _compare_responses(
        self,
        control_type: str,
        control_value: str,
        attack_status: int,
        attack_length: int,
        attack_hash: str,
        control_response: Dict,
    ) -> ControlTestResult:
        """Compare a control response against the attack response."""
        control_status = control_response.get("status", 0)
        control_body = control_response.get("body", "")
        control_length = len(control_body)
        control_hash = hashlib.md5(
            control_body.encode("utf-8", errors="replace")
        ).hexdigest()

        status_match = (attack_status == control_status)

        hash_match = (attack_hash == control_hash)

        if attack_length == 0 and control_length == 0:
            length_similar = True
        elif attack_length == 0 or control_length == 0:
            length_similar = False
        else:
            diff_pct = abs(attack_length - control_length) / max(attack_length, 1) * 100
            length_similar = diff_pct <= self.LENGTH_THRESHOLD_PCT

        same_behavior = status_match and (hash_match or length_similar)

        detail = (f"{control_type}('{control_value[:30]}'): "
                 f"status {'=' if status_match else '!'}= {control_status}, "
                 f"len {control_length} "
                 f"({'same' if length_similar else 'different'} from {attack_length})"
                 f"{', EXACT MATCH' if hash_match else ''}")

        return ControlTestResult(
            control_type=control_type,
            control_value=control_value[:50],
            status_match=status_match,
            length_similar=length_similar,
            hash_match=hash_match,
            same_behavior=same_behavior,
            detail=detail,
        )