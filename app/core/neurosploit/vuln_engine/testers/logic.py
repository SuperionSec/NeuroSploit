"""
NeuroSploit v3 - Business Logic Vulnerability Testers

Testers for Race Condition, Business Logic Flaws, Rate Limit Bypass,
Parameter Pollution, Type Juggling, Timing Attack, Host Header Injection.
"""
import re
from typing import Tuple, Dict, Optional
from app.core.neurosploit.vuln_engine.testers.base_tester import BaseTester


class RaceConditionTester(BaseTester):
    """Tester for Race Condition vulnerabilities"""

    def __init__(self):
        super().__init__()
        self.name = "race_condition"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        if context.get("concurrent_requests"):
            total_requests = context["concurrent_requests"]
            success_count = context.get("success_count", 0)
            failure_count = context.get("failure_count", 0)

            if success_count > 1:
                return True, 0.9, f"Race condition: {success_count}/{total_requests} concurrent requests succeeded"

            if success_count > 0 and context.get("limit_exceeded"):
                return True, 0.85, f"Race condition: Limit bypass with {success_count} successes"

        if response_status in [200, 201]:
            body_lower = response_body.lower()
            success_indicators = [
                r'"success"\s*:\s*true',
                r'"status"\s*:\s*"(?:ok|success|created)"',
                r"transaction\s+(?:successful|completed|processed)",
                r"purchase\s+(?:successful|completed|processed)",
                r"payment\s+(?:successful|completed|processed)",
                r"(?:coupon|voucher|discount)\s+(?:applied|used|redeemed)",
            ]
            for pattern in success_indicators:
                if re.search(pattern, response_body, re.IGNORECASE):
                    return True, 0.6, "Race condition: Successful operation - verify concurrency safety"

        return False, 0.0, None


class BusinessLogicTester(BaseTester):
    """Tester for Business Logic Flaws"""

    def __init__(self):
        super().__init__()
        self.name = "business_logic"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        logic_violations = {
            r'"price"\s*:\s*["\']?0(?:\.00)?["\']?': "Zero price accepted",
            r'"price"\s*:\s*-\d+': "Negative price accepted",
            r'"quantity"\s*:\s*-\d+': "Negative quantity accepted",
            r'"discount"\s*:\s*100': "100% discount accepted",
            r'"discount"\s*:\s*-\d+': "Negative discount (bonus) accepted",
            r'"total"\s*:\s*["\']?0(?:\.00)?["\']?': "Zero total accepted",
            r'"status"\s*:\s*"paid".*"amount"\s*:\s*0': "Zero payment marked as paid",
            r'"verified"\s*:\s*true.*without.*verification': "Unverified accepted",
        }
        for pattern, description in logic_violations.items():
            if re.search(pattern, response_body, re.IGNORECASE):
                return True, 0.85, f"Business logic flaw: {description}"

        if response_status in [200, 201]:
            price_zero = "price" in payload and (":0" in payload or ": 0" in payload)
            negative_qty = "quantity" in payload and ("-1" in payload or "-999" in payload)

            if price_zero or negative_qty:
                return True, 0.7, f"Business logic flaw: Unusual parameters accepted {'(zero price)' if price_zero else '(negative quantity)'}"

            if "free" in response_body.lower() and any(x in payload.lower() for x in ["price", "cost", "amount"]):
                return True, 0.65, "Business logic flaw: Item obtained for free"

        return False, 0.0, None


class RateLimitBypassTester(BaseTester):
    """Tester for Rate Limit Bypass"""

    def __init__(self):
        super().__init__()
        self.name = "rate_limit_bypass"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        if context.get("request_count"):
            total = context["request_count"]
            limited = context.get("limited_count", 0)
            succeeded = context.get("success_count", 0)

            if succeeded > 0 and total > 50:
                return True, 0.8, f"Rate limit bypass: {succeeded}/{total} requests succeeded"

            if limited == 0 and total > 20:
                return True, 0.75, f"Rate limit bypass: No rate limiting after {total} requests"

        rate_limit_headers = ["X-RateLimit-Remaining", "X-Rate-Limit-Remaining", "Rate-Limit-Remaining"]
        for header in rate_limit_headers:
            if header in response_headers:
                remaining = int(response_headers.get(header, 100))
                if remaining > 90 and context.get("request_count", 0) > 20:
                    return True, 0.6, "Rate limit bypass: Rate limit not being decremented"

        if response_status != 429:
            return True, 0.5, "Rate limit: No 429 response after multiple requests"

        return False, 0.0, None


class ParameterPollutionTester(BaseTester):
    """Tester for HTTP Parameter Pollution"""

    def __init__(self):
        super().__init__()
        self.name = "parameter_pollution"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        if "param1=value1&param1=value2" in payload or "param1=value1,param1=value2" in payload:
            if response_status == 200:
                if "value1" in response_body and "value2" in response_body:
                    return True, 0.8, "HPP: Both parameter values processed"

                if "value2" in response_body and "value1" not in response_body:
                    return True, 0.7, "HPP: Last parameter value used (overwrite behavior)"

                if "value1" in response_body and "value2" not in response_body:
                    return True, 0.7, "HPP: First parameter value used"

                if "array" in response_body.lower() or "list" in response_body.lower() or "," in response_body:
                    return True, 0.75, "HPP: Parameters combined into array"

        return False, 0.0, None


class TypeJugglingTester(BaseTester):
    """Tester for PHP Type Juggling"""

    def __init__(self):
        super().__init__()
        self.name = "type_juggling"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        type_juggling_indicators = {
            r'(?:comparison|check)\s+(?:passed|successful)': "Type comparison passed",
            r'"authenticated"\s*:\s*true': "Authentication via type juggling",
            r'"admin"\s*:\s*true': "Admin via type juggling",
            r'"verified"\s*:\s*true': "Verified via type juggling",
            r'"bypassed"\s*:\s*true': "Security check bypassed",
            r"(?:hash|password|token)\s+(?:match|valid|correct)": "Hash comparison bypassed",
        }
        for pattern, description in type_juggling_indicators.items():
            if re.search(pattern, response_body, re.IGNORECASE):
                type_juggling_payloads = ["0e", "0", "true", "false", "null", "[]", "{}"]
                if any(tj in payload for tj in type_juggling_payloads):
                    return True, 0.8, f"Type juggling: {description}"

        if response_status == 200:
            type_juggling_payloads = ["0e", "0", "true", "false", "null", "[]", "{}"]
            if any(tj in payload for tj in type_juggling_payloads):
                if any(x in response_body.lower() for x in ["success", "authenticated", "admin", "valid"]):
                    return True, 0.7, "Type juggling: Successful operation with type juggling payload"

        return False, 0.0, None


class TimingAttackTester(BaseTester):
    """Tester for Timing Attacks"""

    def __init__(self):
        super().__init__()
        self.name = "timing_attack"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        if context.get("response_times"):
            times = context["response_times"]
            avg_time = sum(times) / len(times)

            if context.get("baseline_time"):
                baseline = context["baseline_time"]
                diff = abs(avg_time - baseline)
                if diff > 100:
                    return True, 0.7, f"Timing attack: Response time differs by {diff:.0f}ms from baseline"

            if len(times) >= 2:
                max_time = max(times)
                min_time = min(times)
                diff = max_time - min_time
                if diff > 200:
                    return True, 0.65, f"Timing attack: Response time variance of {diff:.0f}ms"

        if "response_time" in context:
            response_time = context["response_time"]
            if response_time > 1000:
                return True, 0.6, f"Timing attack: Slow response ({response_time:.0f}ms) indicates heavy computation"

        return False, 0.0, None


class HostHeaderInjectionTester(BaseTester):
    """Tester for Host Header Injection"""

    def __init__(self):
        super().__init__()
        self.name = "host_header_injection"

    def build_request(self, endpoint, payload: str) -> Tuple[str, Dict, Dict, Optional[str]]:
        headers = {
            "User-Agent": "NeuroSploit/3.0",
            "Host": payload
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
        if payload in response_body:
            return True, 0.9, "Host header injection: Host value reflected in response"

        host_in_url = re.search(
            rf"https?://{re.escape(payload)}",
            response_body
        )
        if host_in_url:
            return True, 0.85, "Host header injection: Host value used in URL generation"

        evil_in_links = re.search(
            rf'href\s*=\s*["\']https?://{re.escape(payload)}',
            response_body, re.IGNORECASE
        )
        if evil_in_links:
            return True, 0.8, "Host header injection: Host value used in link generation"

        if response_status in [301, 302, 303, 307]:
            location = response_headers.get("Location", "")
            if payload in location:
                return True, 0.75, "Host header injection: Host value used in redirect"

        return False, 0.0, None
