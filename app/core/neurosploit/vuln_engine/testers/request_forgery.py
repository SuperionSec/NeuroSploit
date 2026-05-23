"""
NeuroSploit v3 - Request Forgery Vulnerability Testers

Testers for SSRF, CSRF, and GraphQL introspection/dos.
"""
import re
from typing import Tuple, Dict, Optional
from app.core.neurosploit.vuln_engine.testers.base_tester import BaseTester


class SSRFTester(BaseTester):
    """Tester for Server-Side Request Forgery"""

    def __init__(self):
        super().__init__()
        self.name = "ssrf"
        self.internal_markers = {
            "ssrf_internal",
            "ssrf_test_local",
            "internal_ssrf_test",
        }

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        for marker in self.internal_markers:
            if marker in payload and marker in response_body:
                return True, 0.95, f"SSRF confirmed: Internal response with marker '{marker}'"

        cloud_metadata = {
            "ami-id": "AWS AMI ID",
            "local-ipv4": "AWS local IP",
            "public-ipv4": "AWS public IP",
            "instance-id": "AWS instance ID",
            "hostname": "AWS hostname",
            "vm-id": "Azure VM ID",
            "subscriptionId": "Azure subscription",
        }
        for indicator, desc in cloud_metadata.items():
            if indicator in response_body.lower():
                return True, 0.9, f"SSRF: Cloud metadata exposed - {desc}"

        internal_indicators = [
            "169.254.169.254", "10.0.0.", "172.16.",
            "192.168.", "127.0.0.1", "localhost",
        ]
        for indicator in internal_indicators:
            if indicator in response_body:
                if any(ip in payload for ip in ["169.254", "127.0.0.1", "localhost"]):
                    return True, 0.85, f"SSRF: Internal IP content in response: {indicator}"

        return False, 0.0, None


class CSRFTester(BaseTester):
    """Tester for Cross-Site Request Forgery"""

    def __init__(self):
        super().__init__()
        self.name = "csrf"
        self.state_methods = ["POST", "PUT", "DELETE", "PATCH"]

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        request_method = context.get("method", "GET")

        if request_method not in self.state_methods:
            return False, 0.0, None

        csrf_headers = {
            "x-csrf-token", "x-xsrf-token", "x-csrftoken",
            "csrf-token", "csrf-token-header"
        }
        has_csrf_header = any(
            key.lower() in csrf_headers
            for key in response_headers
        )
        if has_csrf_header:
            return False, 0.0, None

        csrf_params = [
            "csrf_token", "csrf", "xsrf_token", "anti_csrf",
            "csrfmiddlewaretoken", "authenticity_token"
        ]
        has_csrf_param = any(
            param in response_body.lower()
            for param in csrf_params
        )
        if has_csrf_param:
            return False, 0.0, None

        if response_status in [200, 201, 302]:
            success_indicators = [
                r"(?:updated|changed|deleted|created|added|removed)\s+successfully",
                r'"success"\s*:\s*true',
                r'"status"\s*:\s*"(?:ok|success|updated)"',
                r"success(?:fully)?\s+(?:updated|changed|deleted)",
            ]
            for pattern in success_indicators:
                if re.search(pattern, response_body, re.IGNORECASE):
                    return True, 0.8, f"CSRF: State-changing operation succeeded without CSRF token ({request_method})"

            if response_status == 200:
                content_length = int(response_headers.get("Content-Length", 0))
                if content_length > 100 or len(response_body) > 100:
                    return True, 0.7, f"CSRF: {request_method} returned content without CSRF protection"

            if response_status == 302:
                location = response_headers.get("Location", "")
                if "success" in location.lower() or "updated" in location.lower():
                    return True, 0.65, "CSRF: Redirect indicates successful state change"

        return False, 0.0, None


class GraphqlIntrospectionTester(BaseTester):
    """Tester for GraphQL Introspection exposure"""

    def __init__(self):
        super().__init__()
        self.name = "graphql_introspection"

    def build_request(self, endpoint, payload: str) -> Tuple[str, Dict, Dict, Optional[str]]:
        headers = {
            "User-Agent": "NeuroSploit/3.0",
            "Content-Type": "application/json"
        }
        body = '{"query": "{ __schema { queryType { name } } }"}'
        return endpoint.url, {}, headers, body

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        if response_status == 200:
            schema_patterns = [
                r'"__schema"',
                r'"queryType"\s*:',
                r'"mutationType"\s*:',
                r'"subscriptionType"\s*:',
                r'"types"\s*:\s*\[',
                r'"directives"\s*:\s*\[',
            ]
            for pattern in schema_patterns:
                if re.search(pattern, response_body):
                    return True, 0.85, "GraphQL introspection enabled: Schema exposed"

        return False, 0.0, None


class GraphqlDosTester(BaseTester):
    """Tester for GraphQL Denial of Service"""

    def __init__(self):
        super().__init__()
        self.name = "graphql_dos"

    def build_request(self, endpoint, payload: str) -> Tuple[str, Dict, Dict, Optional[str]]:
        headers = {
            "User-Agent": "NeuroSploit/3.0",
            "Content-Type": "application/json"
        }
        body = '{"query": "{ a { b { c { d { e { f { g { h { i { j { k } } } } } } } } } } }"}'
        return endpoint.url, {}, headers, body

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        if response_status in [500, 502, 503, 504]:
            return True, 0.7, "GraphQL DoS: Server error from deep nested query"

        if response_status == 200:
            error_patterns = [
                r"query.*too.*complex",
                r"query.*too.*deep",
                r"maximum.*depth.*exceeded",
                r"complexity.*limit",
            ]
            for pattern in error_patterns:
                if re.search(pattern, response_body, re.IGNORECASE):
                    return False, 0.0, None

        return False, 0.0, None
