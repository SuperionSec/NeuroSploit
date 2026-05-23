"""
NeuroSploit v3 - Advanced Injection Vulnerability Testers

Testers for LDAP Injection, XPath Injection, GraphQL Injection, CRLF Injection,
Header Injection, Email Injection, EL Injection, Log Injection, HTML Injection,
CSV Injection, ORM Injection.
"""
import re
from typing import Tuple, Dict, Optional
from app.core.neurosploit.vuln_engine.testers.base_tester import BaseTester


class LdapInjectionTester(BaseTester):
    """Tester for LDAP Injection"""

    def __init__(self):
        super().__init__()
        self.name = "ldap_injection"
        self.ldap_payloads = [
            "*)(&",
            "*)(uid=*))(|(uid=*",
            "admin*)(&",
            "*)(cn=*))(|(cn=*))",
        ]

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        ldap_errors = [
            r"LDAP.*error",
            r"Invalid DN syntax",
            r"Operations error",
            r"Unwilling to perform",
            r"javax\.naming\.ldap",
            r"ldap_bind",
            r"ldap_search",
        ]
        for pattern in ldap_errors:
            if re.search(pattern, response_body, re.IGNORECASE):
                return True, 0.85, f"LDAP injection: LDAP error triggered - {pattern}"

        if any(bp in payload for bp in self.ldap_payloads):
            if response_status == 200:
                return True, 0.6, "LDAP injection: Successful response after LDAP special chars"

            user_info = re.search(
                r'(?:uid|cn|sn|givenName|mail)\s*[:=]\s*[A-Za-z0-9]+',
                response_body
            )
            if user_info:
                return True, 0.75, "LDAP injection: User data returned"

        return False, 0.0, None


class XpathInjectionTester(BaseTester):
    """Tester for XPath Injection"""

    def __init__(self):
        super().__init__()
        self.name = "xpath_injection"
        self.xpath_payloads = [
            "' or '1'='1",
            "' or 1=1 or '",
            "' or ''='",
            "admin' or '1'='1",
            "'] | //* | //*['",
        ]

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        xpath_errors = [
            r"XPath.*error",
            r"xpath.*evaluation",
            r"Invalid expression",
            r"Undefined variable",
            r"javax\.xml\.xpath",
            r"XPathException",
            r"xpath_error",
        ]
        for pattern in xpath_errors:
            if re.search(pattern, response_body, re.IGNORECASE):
                return True, 0.85, f"XPath injection: XPath error detected - {pattern}"

        if any(bp in payload for bp in self.xpath_payloads):
            if response_status == 200:
                xml_data = re.search(r'<[\w]+>.*</[\w]+>', response_body)
                if xml_data:
                    return True, 0.7, "XPath injection: XML data returned after injection"

                user_data = re.search(
                    r'(?:username|user|name|id|email)\s*[:=]\s*[A-Za-z0-9@.]+',
                    response_body, re.IGNORECASE
                )
                if user_data:
                    return True, 0.75, "XPath injection: User data returned"

        return False, 0.0, None


class GraphqlInjectionTester(BaseTester):
    """Tester for GraphQL Injection"""

    def __init__(self):
        super().__init__()
        self.name = "graphql_injection"

    def build_request(self, endpoint, payload: str) -> Tuple[str, Dict, Dict, Optional[str]]:
        headers = {
            "User-Agent": "NeuroSploit/3.0",
            "Content-Type": "application/json"
        }
        body = payload
        return endpoint.url, {}, headers, body

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        graphql_errors = [
            r'{"errors":\[{"message"',
            r'{"errors":\[{"locations"',
            r'"syntaxError"',
            r'"parse error on input"',
            r"Unexpected .* at",
            r'Bad Request: Unexpected .*',
            r"Cannot query field",
            r'Unknown type',
        ]
        for pattern in graphql_errors:
            if re.search(pattern, response_body, re.IGNORECASE):
                return True, 0.7, f"GraphQL injection: GraphQL error response"

        if '"data"' in response_body and '"errors"' not in response_body:
            if any(injection in payload for injection in ["'", '"', "or 1=1", "union", "--", "#"]):
                return True, 0.65, "GraphQL injection: Query executed with injection payload"

        return False, 0.0, None


class CrlfInjectionTester(BaseTester):
    """Tester for CRLF Injection"""

    def __init__(self):
        super().__init__()
        self.name = "crlf_injection"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        crlf_indicators = {
            r"(?i)Set-Cookie:\s*neurosploit": "Set-Cookie header injected",
            r"(?i)Location:\s*https?://evil\.com": "Location header injected",
            r"(?i)HTTP/1\.\d\s+200": "HTTP response split",
            r"(?i)HTTP/1\.\d\s+301": "HTTP redirect split",
            r"(?i)HTTP/1\.\d\s+302": "HTTP redirect split",
            r"(?i)X-Custom-Header:\s*neurosploit": "Custom header injected",
        }
        for pattern, description in crlf_indicators.items():
            if re.search(pattern, response_body):
                return True, 0.9, f"CRLF injection: {description}"

        response_split = response_body.count("HTTP/1") > 1
        if response_split:
            return True, 0.85, "CRLF injection: HTTP response splitting detected"

        return False, 0.0, None


class HeaderInjectionTester(BaseTester):
    """Tester for HTTP Header Injection"""

    def __init__(self):
        super().__init__()
        self.name = "header_injection"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        header_injection_patterns = {
            r"(?i)X-Forwarded-For:\s*\d+\.\d+\.\d+\.\d+": "X-Forwarded-For injection",
            r"(?i)X-Real-IP:\s*\d+\.\d+\.\d+\.\d+": "X-Real-IP injection",
            r"(?i)X-Originating-IP:\s*\d+\.\d+\.\d+\.\d+": "X-Originating-IP injection",
            r"(?i)Referer:\s*https?://evil\.com": "Referer injection",
            r"(?i)User-Agent:\s*.*<script": "User-Agent XSS injection",
            r"(?i)X-Custom-Header:\s*injected": "Custom header injection",
        }
        for pattern, description in header_injection_patterns.items():
            if re.search(pattern, response_body):
                return True, 0.8, f"Header injection: {description}"

        if context.get("injected_header"):
            if response_status == 200:
                header_name = context["injected_header"]
                if header_name.lower() in response_body.lower():
                    return True, 0.75, f"Header injection: Header '{header_name}' reflected in response"

        return False, 0.0, None


class EmailInjectionTester(BaseTester):
    """Tester for Email Header Injection"""

    def __init__(self):
        super().__init__()
        self.name = "email_injection"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        email_injection_patterns = {
            r"(?i)(?:Bcc|CC|To|From|Subject):\s*\S+@\S+": "Email header injection",
            r"(?i)Content-Type:\s*text/html": "MIME injection",
            r"(?i)MIME-Version:\s*1\.0": "MIME version injection",
            r"(?i)boundary\s*=": "MIME boundary injection",
            r"(?i)(?:sent|delivered|queued).*successfully": "Email injection success",
            r"(?i)mail.*error|smtp.*error": "Email error (potential injection)",
        }
        for pattern, description in email_injection_patterns.items():
            if re.search(pattern, response_body):
                if any(inject in payload for inject in ["\r\n", "\n", "Bcc:", "Cc:", "Content-Type:"]):
                    return True, 0.8, f"Email injection: {description}"

        return False, 0.0, None


class ELInjectionTester(BaseTester):
    """Tester for Expression Language Injection"""

    def __init__(self):
        super().__init__()
        self.name = "el_injection"
        self.el_payloads = [
            "${7*7}",
            "#{7*7}",
            "${'neurosploit'}",
            "#{Runtime.getRuntime().exec('id')}",
            "${''.getClass().forName('java.lang.Runtime')}",
        ]

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        if "49" in response_body and ("${7*7}" in payload or "#{7*7}" in payload):
            return True, 0.9, "EL injection: Math expression evaluated"

        if "neurosploit" in response_body and "${'neurosploit'}" in payload:
            return True, 0.85, "EL injection: String expression evaluated"

        el_errors = [
            r"ELException",
            r"javax\.el\.",
            r"Expression.*error",
            r"EL.*parsing.*error",
            r"PropertyResolver",
        ]
        for pattern in el_errors:
            if re.search(pattern, response_body, re.IGNORECASE):
                return True, 0.75, f"EL injection: Expression Language error - {pattern}"

        return False, 0.0, None


class LogInjectionTester(BaseTester):
    """Tester for Log Injection"""

    def __init__(self):
        super().__init__()
        self.name = "log_injection"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        log_injection_patterns = {
            r"(?i)\[.*\].*\r?\n.*fake\.log": "Log forging",
            r"(?i)\d{4}-\d{2}-\d{2}.*INFO.*fake\.log": "Log timestamp forging",
            r"(?i)ERROR\s+.*\r?\n": "Fake error log entry",
            r"(?i)WARN\s+.*\r?\n": "Fake warning log entry",
            r"(?i)<script>.*alert.*</script>.*\r?\n": "XSS in log entry",
            r"(?i)(?:admin|root).*sudo.*\r?\n": "Fake sudo log entry",
        }
        for pattern, description in log_injection_patterns.items():
            if re.search(pattern, response_body):
                if any(inject in payload for inject in ["\r\n", "\n", "%0d%0a"]):
                    return True, 0.7, f"Log injection: {description}"

        return False, 0.0, None


class HtmlInjectionTester(BaseTester):
    """Tester for HTML Injection"""

    def __init__(self):
        super().__init__()
        self.name = "html_injection"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        html_patterns = {
            r"<img\s+[^>]*src\s*=\s*['\"]https?://evil\.com": "IMG tag injection",
            r"<a\s+[^>]*href\s*=\s*['\"]https?://evil\.com": "Anchor tag injection",
            r"<form\s+[^>]*action\s*=\s*['\"]https?://evil\.com": "Form tag injection",
            r"<iframe\s+[^>]*src\s*=\s*['\"]https?://evil\.com": "IFrame injection",
            r"<style\s*>.*neurosploit.*</style>": "Style tag injection",
            r"<marquee.*>.*neurosploit.*</marquee>": "Marquee tag injection",
            r"<blink.*>.*neurosploit.*</blink>": "Blink tag injection",
            r"<svg.*onload.*alert.*>": "SVG XSS variant",
            r"<video.*onerror.*alert.*>": "Video tag XSS variant",
            r"<audio.*onerror.*alert.*>": "Audio tag XSS variant",
            r"<body.*onload.*alert.*>": "Body onload injection",
        }
        for pattern, description in html_patterns.items():
            if re.search(pattern, response_body, re.IGNORECASE):
                if "neurosploit" in payload or "evil.com" in payload:
                    return True, 0.8, f"HTML injection: {description}"

        if payload in response_body:
            html_tags = ["<img", "<a", "<form", "<iframe", "<style", "<div", "<span", "<marquee"]
            if any(tag in payload.lower() for tag in html_tags):
                return True, 0.7, "HTML injection: HTML tag reflected in response"

        return False, 0.0, None


class CsvInjectionTester(BaseTester):
    """Tester for CSV Injection (Formula Injection)"""

    def __init__(self):
        super().__init__()
        self.name = "csv_injection"
        self.formula_prefixes = ["=", "+", "-", "@", "\t=", "\t+", "\t-"]

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        content_type = response_headers.get("Content-Type", "")
        content_disp = response_headers.get("Content-Disposition", "")

        is_csv = any(ind in content_type.lower() or ind in content_disp.lower() for ind in ["csv", "spreadsheet", "excel"])

        if not is_csv:
            is_csv = any(ext in context.get("endpoint_url", "").lower() for ext in [".csv", ".xls", ".xlsx"])

        if not is_csv:
            return False, 0.0, None

        if any(payload.startswith(prefix) for prefix in self.formula_prefixes):
            if payload in response_body:
                return True, 0.8, "CSV injection: Formula prefix reflected in CSV output"

            calc_patterns = [
                r"cmd\.exe", r"calc\.exe", r"notepad\.exe",
                r"powershell", r"\/bin\/sh", r"\/bin\/bash",
            ]
            for pattern in calc_patterns:
                if re.search(pattern, response_body, re.IGNORECASE):
                    return True, 0.9, f"CSV injection: Formula execution detected - {pattern}"

        return False, 0.0, None


class OrmInjectionTester(BaseTester):
    """Tester for ORM Injection (GORM, Hibernate, Eloquent, etc.)"""

    def __init__(self):
        super().__init__()
        self.name = "orm_injection"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        orm_errors = [
            r"InvalidDataAccessApiUsageException",
            r"QuerySyntaxException",
            r"JPQL.*error",
            r"HQL.*error",
            r"GORM.*error",
            r"Eloquent.*error",
            r"SQLAlchemy.*error",
            r"Django.*ORM.*error",
            r"ActiveRecord.*error",
            r"invalid\s*column\s*name",
            r"could\s*not\s*execute\s*query",
        ]
        for pattern in orm_errors:
            if re.search(pattern, response_body, re.IGNORECASE):
                return True, 0.75, f"ORM injection: ORM error triggered - {pattern}"

        if response_status == 200:
            if any(bp in payload for bp in ["' or '1'='1", "' or 1=1", "or true"]):
                data_patterns = [
                    r'"data"\s*:\s*\[.*\]',
                    r'"results"\s*:\s*\[.*\]',
                    r'"items"\s*:\s*\[.*\]',
                    r'"users"\s*:\s*\[.*\]',
                ]
                for pattern in data_patterns:
                    if re.search(pattern, response_body, re.DOTALL):
                        return True, 0.7, "ORM injection: Full data returned with tautology"

        return False, 0.0, None
