"""
NeuroSploit v3 - Client-Side Vulnerability Testers

Testers for CORS, Clickjacking, Open Redirect, DOM Clobbering, PostMessage,
Websocket Hijacking, Prototype Pollution, CSS Injection, Tabnabbing.
"""
import re
from typing import Tuple, Dict, Optional
from app.core.neurosploit.vuln_engine.testers.base_tester import BaseTester


class CORSTester(BaseTester):
    """Tester for CORS misconfiguration"""

    def __init__(self):
        super().__init__()
        self.name = "cors"

    def build_request(self, endpoint, payload: str) -> Tuple[str, Dict, Dict, Optional[str]]:
        headers = {
            "User-Agent": "NeuroSploit/3.0",
            "Origin": "https://evil.com"
        }
        return endpoint.url, {}, headers, None

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        acao = response_headers.get("Access-Control-Allow-Origin", "")
        if acao == "https://evil.com":
            acac = response_headers.get("Access-Control-Allow-Credentials", "")
            if acac == "true":
                return True, 0.9, "CORS misconfig: Wildcard origin with credentials"

            acam = response_headers.get("Access-Control-Allow-Methods", "")
            if "DELETE" in acam or "PUT" in acam or "PATCH" in acam:
                return True, 0.8, f"CORS misconfig: Permissive origin with dangerous methods: {acam}"

            return True, 0.7, "CORS misconfig: Reflected arbitrary origin"

        acao_header = response_headers.get("Access-Control-Allow-Origin", "")
        if acao_header == "null":
            return True, 0.7, "CORS misconfig: Allows 'null' origin (sandbox iframes)"

        if not acao:
            return False, 0.0, None

        return False, 0.0, None


class ClickjackingTester(BaseTester):
    """Tester for Clickjacking (Missing X-Frame-Options)"""

    def __init__(self):
        super().__init__()
        self.name = "clickjacking"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        xfo = response_headers.get("X-Frame-Options", "")
        csp_frame = response_headers.get("Content-Security-Policy", "")

        if not xfo and "frame-ancestors" not in csp_frame:
            if response_status == 200 and len(response_body) > 100:
                return True, 0.7, "Clickjacking: No frame protection headers"

        return False, 0.0, None


class OpenRedirectTester(BaseTester):
    """Tester for Open Redirect"""

    def __init__(self):
        super().__init__()
        self.name = "open_redirect"
        self.evil_url = "https://evil.com"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        if response_status in [301, 302, 303, 307, 308]:
            location = response_headers.get("Location", "")
            if self.evil_url in location:
                return True, 0.95, f"Open redirect confirmed: {location}"

            if "evil.com" in location:
                return True, 0.9, f"Open redirect confirmed: {location}"

        refresh = response_headers.get("Refresh", "")
        if "evil.com" in refresh:
            return True, 0.8, "Open redirect: Refresh header with external URL"

        redirect_patterns = [
            r'window\.location\s*=\s*["\']https?://evil\.com',
            r'<meta\s+http-equiv\s*=\s*["\']refresh["\'][^>]*evil\.com',
            r'location\.href\s*=\s*["\']https?://evil\.com',
        ]
        for pattern in redirect_patterns:
            if re.search(pattern, response_body, re.IGNORECASE):
                return True, 0.8, "Open redirect: Redirect to external URL in response body"

        return False, 0.0, None


class DomClobberingTester(BaseTester):
    """Tester for DOM Clobbering"""

    def __init__(self):
        super().__init__()
        self.name = "dom_clobbering"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        clobbering_vars = [
            "window.onload", "document.body", "document.location",
            "document.referrer", "document.domain", "document.cookie",
            "window.name", "location.href"
        ]

        for var in clobbering_vars:
            pattern = rf'<[^>]+(?:id|name)\s*=\s*["\']{re.escape(var.split(".")[-1])}["\']'
            if re.search(pattern, response_body):
                script_pattern = rf'<script[^>]*>.*?{re.escape(var)}.*?</script>'
                if re.search(script_pattern, response_body, re.IGNORECASE | re.DOTALL):
                    return True, 0.75, f"DOM clobbering potential: {var} could be overwritten"

        anchor_patterns = [
            r'<a\s+[^>]*(?:id|name)\s*=\s*["\'](?:onload|onerror|onclick)["\']',
            r'<(?:iframe|img|svg|object)\s+[^>]*(?:id|name)\s*=\s*["\'](?:on\w+)["\']',
        ]
        for pattern in anchor_patterns:
            if re.search(pattern, response_body, re.IGNORECASE):
                return True, 0.65, "DOM clobbering: Event handler attribute name found"

        return False, 0.0, None


class PostMessageVulnTester(BaseTester):
    """Tester for PostMessage vulnerabilities"""

    def __init__(self):
        super().__init__()
        self.name = "postmessage_vuln"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        message_patterns = [
            r'addEventListener\s*\(\s*["\']message["\']',
            r'window\.addEventListener\s*\(\s*["\']message["\']',
            r'(?:window\.)?onmessage\s*=\s*',
            r'\$\(window\)\.on\s*\(\s*["\']message["\']',
        ]
        for pattern in message_patterns:
            if re.search(pattern, response_body):
                origin_check_pattern = r'event\.origin\s*(?:===|!==|==|!=)'
                if not re.search(origin_check_pattern, response_body):
                    return True, 0.7, "PostMessage: No origin validation on message event listener"

                insecure_patterns = [
                    r'event\.origin\s*===\s*["\']\*["\']',
                    r'event\.origin\s*!=\s*["\']null["\']',
                    r'event\.origin\s*(?:\.includes|\.indexOf)\s*\(\s*["\']\*["\']',
                ]
                for insecure in insecure_patterns:
                    if re.search(insecure, response_body):
                        return True, 0.8, "PostMessage: Insecure origin validation (wildcard/weak check)"

        return False, 0.0, None


class WebsocketHijackTester(BaseTester):
    """Tester for WebSocket hijacking"""

    def __init__(self):
        super().__init__()
        self.name = "websocket_hijack"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        ws_patterns = [
            r'new\s+WebSocket\s*\(',
            r'new\s+window\.WebSocket\s*\(',
        ]
        for pattern in ws_patterns:
            if re.search(pattern, response_body):
                origin_check_patterns = [
                    r'checkOrigin', r'allowedOrigins', r'validateOrigin',
                    r'origin.*check', r'origin.*valid',
                ]
                has_origin_check = any(re.search(p, response_body, re.IGNORECASE) for p in origin_check_patterns)
                if not has_origin_check:
                    return True, 0.65, "WebSocket: No origin validation detected"

        ws_upgrade = response_headers.get("Upgrade", "")
        if "websocket" in ws_upgrade.lower():
            origin = response_headers.get("Origin", "")
            if origin == "https://evil.com":
                return True, 0.8, "WebSocket: Arbitrary origin accepted for WebSocket connection"

        return False, 0.0, None


class PrototypePollutionTester(BaseTester):
    """Tester for Prototype Pollution"""

    def __init__(self):
        super().__init__()
        self.name = "prototype_pollution"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        if "neurosploit_polluted" in response_body:
            return True, 0.9, "Prototype pollution confirmed: Polluted property reflected"

        prototype_errors = [
            r"prototype.*pollution",
            r"__proto__.*not allowed",
            r"constructor.*not allowed",
        ]
        for pattern in prototype_errors:
            if re.search(pattern, response_body, re.IGNORECASE):
                return True, 0.6, f"Prototype pollution indicator: {pattern}"

        if "isVIP" in payload and "true" in response_body:
            return True, 0.7, "Prototype pollution: Privilege elevation via __proto__"

        return False, 0.0, None


class CssInjectionTester(BaseTester):
    """Tester for CSS Injection"""

    def __init__(self):
        super().__init__()
        self.name = "css_injection"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        if "background-image: url('https://evil.com/css" in response_body:
            return True, 0.85, "CSS injection: External URL in CSS property"

        dangerous_properties = [
            "expression(", "-moz-binding", "url(javascript:",
            "behavior:", "binding:"
        ]
        for prop in dangerous_properties:
            if prop in response_body.lower() and prop in payload.lower():
                return True, 0.7, f"CSS injection: Dangerous property '{prop}'"

        if re.search(r'@import\s+["\']https?://', response_body):
            return True, 0.6, "CSS injection: @import with external URL"

        if re.search(r'url\s*\(\s*["\']?https?://evil\.com', response_body, re.IGNORECASE):
            return True, 0.8, "CSS injection: External resource URL in style"

        return False, 0.0, None


class TabnabbingTester(BaseTester):
    """Tester for Reverse Tabnabbing"""

    def __init__(self):
        super().__init__()
        self.name = "tabnabbing"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        target_blank = re.findall(
            r'<a[^>]*target\s*=\s*["\']_blank["\'][^>]*>',
            response_body, re.IGNORECASE
        )
        if target_blank:
            vulnerable_links = 0
            for link in target_blank:
                has_rel = re.search(r'\brel\s*=', link, re.IGNORECASE)
                has_noreferrer = re.search(
                    r'\brel\s*=\s*["\'][^"\']*\bnoreferrer\b[^"\']*["\']',
                    link, re.IGNORECASE
                )
                has_nofollow = re.search(
                    r'\brel\s*=\s*["\'][^"\']*\bnofollow\b[^"\']*["\']',
                    link, re.IGNORECASE
                )
                has_opener = re.search(
                    r'\brel\s*=\s*["\'][^"\']*\bnoopeners*\b',
                    link, re.IGNORECASE
                )

                if not has_rel or (not has_noreferrer and not has_nofollow and not has_opener):
                    vulnerable_links += 1

            if vulnerable_links > 0:
                return True, 0.7, f"Tabnabbing: {vulnerable_links} target='_blank' links without rel='noopener noreferrer'"

        return False, 0.0, None
