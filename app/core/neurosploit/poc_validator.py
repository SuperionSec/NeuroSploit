"""
PoC Validator — validates Proof-of-Concept payloads for discovered vulnerabilities.

Ensures generated PoCs are:
- Correctly formed (syntax check)
- Self-contained (no external deps unless needed)
- Safe (no destructive payloads)
- Reproducible (can be executed without modification)
"""

import re
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from enum import Enum


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class PoCStatus(Enum):
    VALID = "valid"
    WARNING = "warning"
    INVALID = "invalid"
    UNSAFE = "unsafe"


class ValidationCheck(Enum):
    """Individual validation checks."""
    SYNTAX = "syntax"
    SELF_CONTAINED = "self_contained"
    SAFETY = "safety"
    REPRODUCIBILITY = "reproducibility"
    COMPLETENESS = "completeness"
    PAYLOAD_INTEGRITY = "payload_integrity"
    HEADER_VALIDITY = "header_validity"
    URL_VALIDITY = "url_validity"
    METHOD_VALIDITY = "method_validity"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class ValidationIssue:
    """A single issue found during PoC validation."""
    check: str  # ValidationCheck enum value
    severity: str  # error, warning, info
    message: str
    location: str = ""  # where in the PoC (script, curl, etc.)
    suggestion: str = ""


@dataclass
class PoCValidationResult:
    """Result of a PoC validation run."""
    status: str = "valid"  # PoCStatus enum value
    issues: List[ValidationIssue] = field(default_factory=list)
    checks_passed: int = 0
    checks_failed: int = 0
    checks_warning: int = 0
    suggestions: List[str] = field(default_factory=list)
    is_executable: bool = False
    is_safe: bool = True


# ---------------------------------------------------------------------------
# Destructive / Dangerous Payload Patterns
# ---------------------------------------------------------------------------

DESTRUCTIVE_PATTERNS = [
    # SQL
    r"\bDROP\s+(TABLE|DATABASE|INDEX|VIEW|PROCEDURE|FUNCTION|TRIGGER)\b",
    r"\bDELETE\s+FROM\b",
    r"\bTRUNCATE\s+(TABLE\s+)?\b",
    r"\bALTER\s+(TABLE|DATABASE)\s+\w+\s+DROP\b",
    r"\bUPDATE\s+\w+\s+SET\b",
    r"\bINSERT\s+INTO\b",
    r"\bEXEC\s*(\(|sp_)",
    r"\bxp_cmdshell\b",
    r"\bSHUTDOWN\b",

    # OS Command
    r"\brm\s+-rf\b",
    r"\bdd\s+if=",
    r"\bmkfs\.",
    r"\b:\(\)\s*\{",
    r"\bchmod\s+(777|000)",
    r"\breboot\b",
    r"\bshutdown\b",
    r"\bpoweroff\b",
    r"\bkill\s+-9\b",
    r"\bdel\s+/[fsq]\s+",

    # File system
    r"/etc/(?:passwd|shadow|sudoers)",
    r"\.\./\.\./(?:etc|var|proc|dev|sys)",
    r"file:///(?:etc|proc|dev)",

    # Network
    r"\bwget\s+.*\|\s*(?:sh|bash)",
    r"\bcurl\s+.*\|\s*(?:sh|bash)",
    r"\bnc\s+-l",
    r"\bnetcat\s+-l",
]


# ---------------------------------------------------------------------------
# Required Elements by Vulnerability Category
# ---------------------------------------------------------------------------

REQUIRED_ELEMENTS = {
    "xss": {
        "payload_patterns": [
            r"alert\s*\(",
            r"prompt\s*\(",
            r"confirm\s*\(",
            r"document\.cookie",
            r"onerror\s*=",
            r"onload\s*=",
            r"<script",
            r"eval\s*\(",
        ],
        "required_fields": ["payload", "url"],
    },
    "sqli": {
        "payload_patterns": [
            r"(?:SELECT|UNION(?:\s+ALL)?\s+SELECT)",
            r"(?:OR|AND)\s+[\d'\"].*=\s*[\d'\"]",
            r"sleep\s*\(",
            r"BENCHMARK\s*\(",
            r"WAITFOR\s+DELAY",
        ],
        "required_fields": ["payload", "url"],
    },
    "ssti": {
        "payload_patterns": [
            r"\{\{.*\}\}",
            r"\$\{.*\}",
            r"<%=.*%>",
        ],
        "required_fields": ["payload", "url"],
    },
    "ssrf": {
        "payload_patterns": [
            r"https?://",
            r"localhost",
            r"127\.0\.0\.1",
            r"169\.254\.169\.254",
        ],
        "required_fields": ["payload", "url"],
    },
    "lfi": {
        "payload_patterns": [
            r"\.\./",
            r"etc/passwd",
            r"etc/shadow",
            r"php://",
            r"file://",
        ],
        "required_fields": ["payload", "url"],
    },
    "open_redirect": {
        "payload_patterns": [
            r"https?://",
            r"redirect",
        ],
        "required_fields": ["payload", "url", "redirect_url"],
    },
}

# Safe (informational-only) XSS payload patterns
SAFE_XSS_PATTERNS = [
    r"alert\s*\(\s*1\s*\)",
    r"alert\s*\(\s*['\"]XSS['\"]\s*\)",
    r"alert\s*\(\s*document\.domain\s*\)",
    r"alert\s*\(\s*['\"]PoC['\"]\s*\)",
    r"alert\s*\(\s*['\"]NeuroSploit['\"]\s*\)",
    r"alert\s*\(\s*['\"]test['\"]\s*\)",
    r"prompt\s*\(\s*1\s*\)",
    r"confirm\s*\(\s*1\s*\)",
    r"document\.write\s*\(\s*['\"]XSS['\"]\s*\)",
]


# ---------------------------------------------------------------------------
# PoC Validator
# ---------------------------------------------------------------------------

class PoCValidator:
    """Validates PoC payloads for correctness, safety, and reproducibility."""

    def __init__(self):
        self._validation_cache: Dict[str, PoCValidationResult] = {}

    # ── Full Validation Pipeline ───────────────────────────────────────

    def validate(
        self, poc: Dict, category: Optional[str] = None,
    ) -> PoCValidationResult:
        """Run full validation pipeline on a PoC."""
        result = PoCValidationResult()

        # Determine category
        cat = (category or
               poc.get("category") or
               poc.get("type") or
               "unknown").lower()

        # Run all checks
        checks = [
            self._check_syntax(poc, result),
            self._check_self_contained(poc, result),
            self._check_safety(poc, cat, result),
            self._check_reproducibility(poc, result),
            self._check_completeness(poc, cat, result),
            self._check_payload_integrity(poc, cat, result),
            self._check_url_validity(poc, result),
            self._check_method_validity(poc, result),
        ]

        # Aggregate
        for issue in checks:
            if issue.severity == "error":
                result.checks_failed += 1
            elif issue.severity == "warning":
                result.checks_warning += 1
            else:
                result.checks_passed += 1

        result.checks_passed += sum(
            1 for c in checks if c.severity == "info"
        )

        # Determine overall status
        if any(issue.severity == "error" for issue in checks):
            result.status = "invalid"
        elif any(issue.severity == "warning" for issue in checks):
            result.status = "warning"
        else:
            result.status = "valid"

        # Determine executability
        result.is_executable = (
            result.status in ("valid", "warning") and
            poc.get("url") and
            poc.get("payload") or poc.get("curl_command")
        )

        result.is_safe = result.status != "unsafe"

        # Collect suggestions
        result.suggestions = [
            issue.suggestion for issue in checks
            if issue.suggestion and issue.severity in ("warning", "error")
        ]

        return result

    def validate_batch(
        self, pocs: List[Dict], category: Optional[str] = None,
    ) -> List[PoCValidationResult]:
        """Validate multiple PoCs."""
        return [self.validate(poc, category) for poc in pocs]

    def is_safe_payload(self, payload: str, category: str) -> bool:
        """Check if a payload is safe for execution."""
        result = PoCValidationResult()
        issue = self._check_safety({"payload": payload}, category, result)
        return issue.severity != "error"

    def sanitize_payload(self, payload: str, category: str) -> str:
        """Sanitize a payload to make it safe."""
        # Remove common dangerous commands
        sanitized = payload

        # Replace destructive SQL commands with SELECT queries
        if category == "sqli":
            sanitized = re.sub(
                r"\b(DROP|DELETE|TRUNCATE|ALTER|UPDATE|INSERT|EXEC|SHUTDOWN)\b",
                "SELECT", sanitized, flags=re.IGNORECASE,
            )

        # Replace dangerous OS commands
        dangerous_commands = [
            "rm -rf", "shutdown", "reboot", "poweroff",
            "dd if=", "mkfs.", "kill -9", "chmod 777",
            "del /f", "format c:",
        ]
        for cmd in dangerous_commands:
            if cmd.lower() in sanitized.lower():
                sanitized = sanitized.replace(cmd, "echo SAFE")

        # Replace cookie stealing with alert
        if "document.cookie" in sanitized:
            sanitized = sanitized.replace(
                "document.cookie", "'PoC_TEST_COOKIE'"
            )

        return sanitized

    # ── Individual Checks ──────────────────────────────────────────────

    def _check_syntax(
        self, poc: Dict, result: PoCValidationResult,
    ) -> ValidationIssue:
        """Check PoC syntax and structure."""
        issue = ValidationIssue(
            check="syntax", severity="info",
            message="Syntax check passed.",
        )

        # Check for required top-level keys
        required_keys = {"payload", "url"}
        poc_keys = set(poc.keys())
        if not (required_keys & poc_keys) and "curl_command" not in poc:
            issue.severity = "error"
            issue.message = "PoC missing required fields: must contain 'url' and 'payload' or 'curl_command'."
            issue.suggestion = "Add 'url' and 'payload' fields to the PoC."
            return issue

        # Check payload is not empty
        payload = poc.get("payload", poc.get("value", ""))
        if payload and not isinstance(payload, str):
            issue.severity = "error"
            issue.message = "Payload must be a string."
            return issue

        # Check URL is not empty
        url = poc.get("url", poc.get("target", ""))
        if url and not isinstance(url, str):
            issue.severity = "error"
            issue.message = "URL must be a string."
            return issue

        return issue

    def _check_self_contained(
        self, poc: Dict, result: PoCValidationResult,
    ) -> ValidationIssue:
        """Check that the PoC is self-contained."""
        issue = ValidationIssue(
            check="self_contained", severity="info",
            message="PoC is self-contained.",
        )

        # Check for external dependency references
        payload = str(poc.get("payload", poc.get("value", "")))
        if not payload:
            return issue

        external_patterns = [
            r"require\s*\(\s*['\"]\w",
            r"import\s+\w+\s+from",
            r"from\s+\w+\s+import",
            r"<script\s+src=",
        ]

        for pattern in external_patterns:
            if re.search(pattern, payload):
                issue.severity = "warning"
                issue.message = f"Payload may reference external dependencies: '{pattern}'"
                issue.suggestion = "Make payload self-contained or note the dependency."
                return issue

        return issue

    def _check_safety(
        self, poc: Dict, category: str, result: PoCValidationResult,
    ) -> ValidationIssue:
        """Check for destructive or dangerous payload content."""
        issue = ValidationIssue(
            check="safety", severity="info",
            message="Payload is safe.",
        )

        payload = str(poc.get("payload", poc.get("value", "")))
        if not payload:
            return issue

        # Check for destructive patterns
        for pattern in DESTRUCTIVE_PATTERNS:
            if re.search(pattern, payload, re.IGNORECASE):
                issue.severity = "error"
                issue.message = f"Payload contains destructive command: '{pattern}'."
                issue.suggestion = (
                    "Replace destructive commands with read-only operations "
                    "(e.g., use SELECT instead of DELETE, alert() instead of "
                    "cookie stealing)."
                )
                return issue

        # For XSS, check payload is non-destructive
        if category == "xss":
            # Allow common safe XSS patterns
            is_safe = any(
                re.search(p, payload, re.IGNORECASE)
                for p in SAFE_XSS_PATTERNS
            )
            if not is_safe:
                # Check if it's a simple script tag
                if re.search(r"<\s*script\s*>[\s\w();]*<\s*/\s*script\s*>", payload):
                    is_safe = True

            if not is_safe:
                issue.severity = "warning"
                issue.message = "XSS payload may not be innocuous — verify it only demonstrates XSS, doesn't steal data."
                issue.suggestion = "Use alert(1), alert(document.domain), or prompt('XSS') for safe PoCs."

        # For SSRF, check target is safe
        if category == "ssrf":
            safe_targets = ["localhost", "127.0.0.1", "169.254.169.254",
                           "burpcollaborator.net", "webhook.site",
                           "requestbin.com", "interact.sh", "hookbin.com"]
            if not any(t in payload.lower() for t in safe_targets):
                issue.severity = "warning"
                issue.message = "SSRF payload targets an unknown host — verify this is safe and intentional."
                issue.suggestion = "Use a controlled callback service (e.g., Burp Collaborator) for PoC."

        return issue

    def _check_reproducibility(
        self, poc: Dict, result: PoCValidationResult,
    ) -> ValidationIssue:
        """Check that the PoC is reproducible."""
        issue = ValidationIssue(
            check="reproducibility", severity="info",
            message="PoC is reproducible.",
        )

        # Check for hardcoded, non-reproducible values
        payload = str(poc.get("payload", poc.get("value", "")))

        # Check for timestamps
        timestamp_patterns = [
            r"\d{10,13}",  # Unix timestamps
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",  # ISO format
        ]
        for tp in timestamp_patterns:
            if re.search(tp, payload):
                issue.severity = "warning"
                issue.message = "Payload contains timestamp — may not be reproducible after expiration."
                issue.suggestion = "Replace time-sensitive values with static placeholders."
                return issue

        # Check for session-specific tokens
        token_patterns = [
            r"[a-f0-9]{32,}",  # MD5/SHA hashes
            r"eyJ[a-zA-Z0-9_-]{20,}\.[a-zA-Z0-9_-]{20,}",  # JWT
        ]
        for tp in token_patterns:
            if re.search(tp, payload):
                issue.severity = "info"
                issue.message = "Payload contains potential session token — may not be reproducible."
                return issue

        # Check that HTTP method is specified
        method = poc.get("method", "").upper()
        if method and method not in ("GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"):
            issue.severity = "warning"
            issue.message = f"Unknown HTTP method: {method}"
            issue.suggestion = "Use a standard HTTP method (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)."
            return issue

        return issue

    def _check_completeness(
        self, poc: Dict, category: str, result: PoCValidationResult,
    ) -> ValidationIssue:
        """Check that the PoC has all required elements for its category."""
        issue = ValidationIssue(
            check="completeness", severity="info",
            message="PoC is complete.",
        )

        if category not in REQUIRED_ELEMENTS:
            return issue

        req = REQUIRED_ELEMENTS[category]
        poc_payload = str(poc.get("payload", poc.get("value", "")))

        # Check required fields
        for field in req.get("required_fields", []):
            if not poc.get(field):
                issue.severity = "warning"
                issue.message = f"PoC missing required field: '{field}'."
                issue.suggestion = f"Add the '{field}' field to the PoC."
                return issue

        # Check payload matches expected patterns
        found_pattern = any(
            re.search(p, poc_payload, re.IGNORECASE)
            for p in req.get("payload_patterns", [])
        )

        if not found_pattern:
            issue.severity = "warning"
            issue.message = f"Payload does not match expected patterns for {category.upper()}."
            issue.suggestion = f"Verify the payload is correct for {category.upper()}."
            return issue

        return issue

    def _check_payload_integrity(
        self, poc: Dict, category: str, result: PoCValidationResult,
    ) -> ValidationIssue:
        """Check that the payload has not been corrupted."""
        issue = ValidationIssue(
            check="payload_integrity", severity="info",
            message="Payload integrity verified.",
        )

        payload = str(poc.get("payload", poc.get("value", "")))
        if not payload:
            return issue

        # Check for double encoding
        double_pct = re.search(r"%25\d{2}", payload)
        if double_pct:
            issue.severity = "warning"
            issue.message = "Payload appears to be double URL-encoded."
            issue.suggestion = "Ensure the payload is only encoded once."
            return issue

        # Check for unclosed tags
        if category == "xss":
            tag_matches = re.findall(r'<(\s*)(\w+)(\s*[^>]*)?>', payload)
            close_matches = re.findall(r'</\s*(\w+)\s*>', payload)

            open_tags = set(name.lower() for _, name, _ in tag_matches if name.lower() not in ('img', 'input', 'br', 'hr', 'meta', 'link', 'source'))
            close_tags = set(name.lower() for name in close_matches)

            unclosed = open_tags - close_tags
            if unclosed:
                issue.severity = "info"
                issue.message = f"Self-closing or unclosed tag detected: {', '.join(unclosed)}. This may be intentional for XSS."

        # Check for unicode corruption
        try:
            payload.encode('utf-8')
        except UnicodeEncodeError:
            issue.severity = "error"
            issue.message = "Payload contains invalid UTF-8 characters."
            issue.suggestion = "Ensure the payload is properly UTF-8 encoded."
            return issue

        return issue

    def _check_url_validity(
        self, poc: Dict, result: PoCValidationResult,
    ) -> ValidationIssue:
        """Check that the target URL is valid."""
        issue = ValidationIssue(
            check="url_validity", severity="info",
            message="URL is valid.",
        )

        url = poc.get("url", poc.get("target", ""))
        if not url:
            return ValidationIssue(
                check="url_validity",
                severity="info",
                message="No URL to validate.",
            )

        # Basic URL format check
        url_pattern = r'^https?://[\w\-.]+(:\d+)?(/.+)?$'
        if not re.match(url_pattern, url, re.IGNORECASE):
            issue.severity = "warning"
            issue.message = f"URL has unusual format: {url}"
            issue.suggestion = "Ensure URL starts with http:// or https:// and has a valid hostname."
            return issue

        return issue

    def _check_method_validity(
        self, poc: Dict, result: PoCValidationResult,
    ) -> ValidationIssue:
        """Check that the HTTP method is valid."""
        issue = ValidationIssue(
            check="method_validity", severity="info",
            message="HTTP method is valid.",
        )

        method = poc.get("method", "").upper()
        if not method:
            return issue

        valid_methods = {"GET", "POST", "PUT", "DELETE", "PATCH",
                        "HEAD", "OPTIONS", "TRACE", "CONNECT"}

        if method not in valid_methods:
            issue.severity = "error"
            issue.message = f"Invalid HTTP method: '{method}'"
            issue.suggestion = f"Use one of: {', '.join(sorted(valid_methods))}"
            return issue

        return issue

    # ── Summary Generation ─────────────────────────────────────────────

    def generate_validation_summary(
        self, results: List[PoCValidationResult],
    ) -> Dict:
        """Generate a summary of all validation results."""
        total = len(results)
        valid = sum(1 for r in results if r.status == "valid")
        warnings = sum(1 for r in results if r.status == "warning")
        invalid = sum(1 for r in results if r.status in ("invalid", "unsafe"))

        all_issues = []
        for r in results:
            all_issues.extend(r.issues)

        # Group issues by severity
        errors = [i for i in all_issues if i.severity == "error"]
        warns = [i for i in all_issues if i.severity == "warning"]
        infos = [i for i in all_issues if i.severity == "info"]

        return {
            "total_pocs": total,
            "valid": valid,
            "warnings": warnings,
            "invalid": invalid,
            "pass_rate": round(valid / total * 100, 1) if total else 0,
            "total_issues": len(all_issues),
            "errors": len(errors),
            "warnings": len(warns),
            "info": len(infos),
            "top_issues": [e.message for e in errors[:5]],
            "top_warnings": [w.message for w in warns[:5]],
            "all_suggestions": sorted(set(
                i.suggestion for i in all_issues if i.suggestion
            )),
        }