"""
NeuroSploit v3 - Infrastructure Vulnerability Testers

Testers for Security Headers, SSL/TLS, HTTP Methods, Directory Listing, Debug Mode,
Exposed Admin Panel, Exposed API Docs, Insecure Cookie Flags.
"""
import re
from typing import Tuple, Dict, Optional
from app.core.neurosploit.vuln_engine.testers.base_tester import BaseTester


class SecurityHeadersTester(BaseTester):
    """Tester for Missing Security Headers"""

    def __init__(self):
        super().__init__()
        self.name = "security_headers"
        self.security_headers = {
            "Content-Security-Policy": {
                "severity": "medium",
                "description": "Missing CSP allows XSS attacks"
            },
            "X-XSS-Protection": {
                "severity": "low",
                "description": "Missing XSS protection header"
            },
            "X-Content-Type-Options": {
                "severity": "low",
                "description": "Missing MIME type sniffing protection"
            },
            "Strict-Transport-Security": {
                "severity": "high",
                "description": "Missing HSTS allows downgrade attacks"
            },
            "X-Frame-Options": {
                "severity": "medium",
                "description": "Missing X-Frame-Options allows clickjacking"
            },
            "Referrer-Policy": {
                "severity": "low",
                "description": "Missing Referrer-Policy leaks sensitive URLs"
            },
            "Permissions-Policy": {
                "severity": "low",
                "description": "Missing Permissions-Policy"
            },
        }

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        missing = []
        for header, info in self.security_headers.items():
            if header not in response_headers:
                missing.append(f"{header} ({info['description']})")

        if missing:
            return True, 0.6, f"Missing security headers: {', '.join(missing[:3])}"

        return False, 0.0, None


class SSLTester(BaseTester):
    """Tester for SSL/TLS configuration issues"""

    def __init__(self):
        super().__init__()
        self.name = "ssl"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        mixed_content = re.findall(
            r'(?:src|href|action)\s*=\s*["\']http://[^"\']+',
            response_body, re.IGNORECASE
        )
        if mixed_content:
            return True, 0.7, f"SSL: {len(mixed_content)} mixed content references"

        hsts = response_headers.get("Strict-Transport-Security", "")
        if not hsts:
            return True, 0.5, "SSL: No HSTS header - missing HTTP Strict Transport Security"

        csp_upgrade = response_headers.get("Content-Security-Policy", "")
        if "upgrade-insecure-requests" not in csp_upgrade.lower():
            return True, 0.4, "SSL: No upgrade-insecure-requests directive in CSP"

        return False, 0.0, None


class HTTPMethodsTester(BaseTester):
    """Tester for Unsafe HTTP Methods"""

    def __init__(self):
        super().__init__()
        self.name = "http_methods"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        allow_header = response_headers.get("Allow", "")
        if allow_header:
            methods = [m.strip().upper() for m in allow_header.split(",")]
            dangerous = ["TRACE", "TRACK", "DELETE", "PUT"]
            enabled_dangerous = [m for m in dangerous if m in methods]
            if enabled_dangerous:
                return True, 0.8, f"Unsafe HTTP methods enabled: {', '.join(enabled_dangerous)}"

        return False, 0.0, None


class DirectoryListingTester(BaseTester):
    """Tester for Directory Listing"""

    def __init__(self):
        super().__init__()
        self.name = "directory_listing"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        if response_status == 200:
            listing_indicators = [
                r"<title>.*(?:index of|directory listing for).*</title>",
                r"<h1>.*(?:index of|directory).*</h1>",
                r"(?:Parent\s+Directory|Last\s+modified|Size|Description)",
                r'<a\s+href=".*\.(?:php|asp|aspx|js|css|txt|sql|bak|log)"[^>]*>',
            ]
            for pattern in listing_indicators:
                if re.search(pattern, response_body, re.IGNORECASE):
                    return True, 0.8, "Directory listing enabled"

            file_listing_patterns = [
                r'\[\s*(?:DIR|<DIR>)\s*\]',
                r'<td[^>]*class="[^"]*file[^"]*"[^>]*>',
                r'<li><a\s+href="[^"]+\.\w+"',
            ]
            for pattern in file_listing_patterns:
                if re.search(pattern, response_body, re.IGNORECASE):
                    return True, 0.6, "Possible directory listing"

        return False, 0.0, None


class DebugModeTester(BaseTester):
    """Tester for Debug Mode exposure"""

    def __init__(self):
        super().__init__()
        self.name = "debug_mode"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        debug_indicators = [
            r"<title>Django.*Debug</title>",
            r"Debug\s+Trace\s+Console",
            r"Traceback \(most recent call last\)",
            r"File \".*\", line \d+, in",
            r"\.env.*APP_DEBUG.*true",
            r"DEBUG\s*=\s*true",
            r"Environment\s*:\s*development",
            r"Application\s+in\s+debug\s+mode",
            r"phpinfo\(\)",
        ]
        for pattern in debug_indicators:
            if re.search(pattern, response_body, re.IGNORECASE):
                return True, 0.9, "Debug mode enabled - sensitive information exposed"

        if response_status in [500, 502, 503]:
            stack_trace = re.search(r'(?:trace|stack)\s*:\s*\[', response_body, re.IGNORECASE)
            if stack_trace:
                return True, 0.7, "Stack trace exposed in error response"

        return False, 0.0, None


class ExposedAdminPanelTester(BaseTester):
    """Tester for Exposed Admin Panel"""

    def __init__(self):
        super().__init__()
        self.name = "exposed_admin_panel"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        if response_status == 200:
            admin_content = [
                r"(?:admin|management|dashboard)\s+(?:panel|console|portal|interface)",
                r"welcome\s+to\s+(?:django|rails|wordpress|drupal|joomla)\s+admin",
                r"admin\s+dashboard",
                r"user\s+management",
                r"system\s+configuration",
                r'<title>.*(?:admin|dashboard|cpanel|phpmyadmin|webmin).*</title>',
            ]
            for pattern in admin_content:
                if re.search(pattern, response_body, re.IGNORECASE):
                    return True, 0.7, "Admin panel accessible without authentication"

        return False, 0.0, None


class ExposedApiDocsTester(BaseTester):
    """Tester for Exposed API Documentation"""

    def __init__(self):
        super().__init__()
        self.name = "exposed_api_docs"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        api_doc_indicators = [
            r"swagger.*ui",
            r"redoc.*ui",
            r"api.*documentation",
            r"openapi.*specification",
            r"interactive.*api.*doc",
            r"try\s+it\s+out",
            r"authorize\s+button",
            r'["\']swagger["\']\s*:',
            r'["\']openapi["\']\s*:\s*["\']3',
            r'["\']info["\']\s*:\s*\{',
            r'["\']paths["\']\s*:\s*\{',
            r'<div[^>]*id\s*=\s*["\']swagger',
        ]
        for pattern in api_doc_indicators:
            if re.search(pattern, response_body, re.IGNORECASE):
                return True, 0.7, "API documentation exposed without authentication"

        return False, 0.0, None


class InsecureCookieFlagsTester(BaseTester):
    """Tester for Insecure Cookie Flags"""

    def __init__(self):
        super().__init__()
        self.name = "insecure_cookie_flags"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        set_cookie = response_headers.get("Set-Cookie", "")

        if set_cookie:
            issues = []
            if "Secure" not in set_cookie:
                issues.append("missing Secure flag")
            if "HttpOnly" not in set_cookie:
                issues.append("missing HttpOnly flag")
            if "SameSite" not in set_cookie:
                issues.append("missing SameSite flag")

            if issues:
                cookie_name = set_cookie.split("=")[0] if "=" in set_cookie else "cookie"
                return True, 0.7, f"Insecure cookie '{cookie_name}': {', '.join(issues)}"

        return False, 0.0, None
