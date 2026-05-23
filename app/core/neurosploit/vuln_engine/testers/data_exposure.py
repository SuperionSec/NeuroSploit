"""
NeuroSploit v3 - Data Exposure Vulnerability Testers

Testers for Sensitive Data Exposure, Information Disclosure, API Key Exposure,
Source Code Disclosure, Backup File Exposure, Version Disclosure.
"""
import re
import base64
from typing import Tuple, Dict, Optional
from app.core.neurosploit.vuln_engine.testers.base_tester import BaseTester


class SensitiveDataExposureTester(BaseTester):
    """Tester for Sensitive Data Exposure"""

    def __init__(self):
        super().__init__()
        self.name = "sensitive_data_exposure"
        self.sensitive_patterns = {
            r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b": "Credit card number",
            r"\b\d{3}-\d{2}-\d{4}\b": "SSN",
            r"(?:password|passwd|pwd)\s*[:=]\s*\S+": "Password in response",
            r"(?:email|mail)\s*:\s*[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}": "Email address",
            r"(?:phone|tel|mobile)\s*:\s*\+?\d{10,}": "Phone number",
            r"(?:ssn|social)\s*:\s*\d{3}-?\d{2}-?\d{4}": "SSN",
            r"(?:api_key|api_secret)\s*:\s*\S+": "API credentials",
        }

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        for pattern, description in self.sensitive_patterns.items():
            if re.search(pattern, response_body):
                return True, 0.8, f"Sensitive data exposed: {description}"

        return False, 0.0, None


class InformationDisclosureTester(BaseTester):
    """Tester for Information Disclosure"""

    def __init__(self):
        super().__init__()
        self.name = "information_disclosure"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        stack_traces = [
            r"Traceback \(most recent call last\)",
            r"at [a-zA-Z0-9_]+\.[a-zA-Z0-9_]+\(",
            r"Caused by:",
            r"Exception in thread",
            r"Fatal error:",
            r"Parse error:",
        ]
        for pattern in stack_traces:
            if re.search(pattern, response_body):
                return True, 0.8, "Information disclosure: Stack trace or error details exposed"

        server_header = response_headers.get("Server", "")
        x_powered_by = response_headers.get("X-Powered-By", "")
        if server_header or x_powered_by:
            return True, 0.5, f"Information disclosure: Server={server_header}, X-Powered-By={x_powered_by}"

        return False, 0.0, None


class ApiKeyExposureTester(BaseTester):
    """Tester for API Key/Secret Exposure"""

    def __init__(self):
        super().__init__()
        self.name = "api_key_exposure"
        self.api_key_patterns = {
            r"(?:AKIA|ABIA|ACCA|ASIA)[A-Z0-9]{16}": "AWS Access Key",
            r"AIza[0-9A-Za-z\\-_]{35}": "Google API Key",
            r"sk-[0-9a-zA-Z\\-_]{32,}": "OpenAI/Stripe API Key",
            r"ghp_[0-9a-zA-Z]{36}": "GitHub Personal Access Token",
            r"xoxb-[0-9a-zA-Z-]{10,}": "Slack Bot Token",
            r"(?:sk|rk)_[0-9a-zA-Z]{24,}": "API key (generic)",
            r"Bearer\s+[A-Za-z0-9\\-._~+/]+=*": "Bearer token",
            r"(?i)(?:aws_access_key_id|aws_secret_access_key)\s*=\s*[A-Za-z0-9/+=]{16,}": "AWS credentials",
            r"(?i)(?:private_key|secret_key|api_key|apikey)\s*[:=]\s*['\"]?[A-Za-z0-9+/=_-]{16,}['\"]?": "API key/secret",
        }

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        for pattern, description in self.api_key_patterns.items():
            match = re.search(pattern, response_body)
            if match:
                return True, 0.85, f"API key exposed: {description}"

        headers_to_check = ["X-API-Key", "Authorization", "X-Access-Token"]
        for header in headers_to_check:
            if header in response_headers:
                return True, 0.7, f"API key/secret in header: {header}"

        return False, 0.0, None


class SourceCodeDisclosureTester(BaseTester):
    """Tester for Source Code Disclosure"""

    def __init__(self):
        super().__init__()
        self.name = "source_code_disclosure"
        self.source_indicators = {
            r"<\?php": "PHP source code",
            r"function\s+\w+\s*\(": "Function definition",
            r"class\s+\w+\s*[{:]": "Class definition",
            r"import\s+\w+\s+from\s+['\"]": "Python import",
            r"const\s+\w+\s*=": "JavaScript const",
            r"let\s+\w+\s*=": "JavaScript let",
            r"var\s+\w+\s*=": "JavaScript var",
            r"(?:public|private|protected)\s+function": "PHP method",
            r"def\s+\w+\s*\(": "Python function",
            r"<%@\s+Page\s+Language": "ASP.NET directive",
        }

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        content_type = response_headers.get("Content-Type", "")
        if "text/plain" in content_type or "application/octet-stream" in content_type:
            for pattern, desc in self.source_indicators.items():
                if re.search(pattern, response_body):
                    return True, 0.85, f"Source code disclosure: {desc}"

        if "Content-Type" not in response_headers or "text/html" not in content_type:
            code_lines = 0
            for pattern in self.source_indicators:
                matches = re.findall(pattern, response_body)
                code_lines += len(matches)
            if code_lines >= 3:
                return True, 0.7, f"Source code disclosure: {code_lines} code patterns found"

        return False, 0.0, None


class BackupFileExposureTester(BaseTester):
    """Tester for Backup File Exposure"""

    def __init__(self):
        super().__init__()
        self.name = "backup_file_exposure"
        self.backup_extensions = [
            ".bak", ".backup", ".old", ".orig", ".save",
            ".tmp", ".temp", ".copy", ".swp",
        ]
        self.backup_indicators = {
            r"\.sql\b": "SQL dump file",
            r"\.tar\.gz\b": "Compressed archive",
            r"\.zip\b": "ZIP archive",
            r"\.rar\b": "RAR archive",
            r"\.env\b": "Environment file",
            r"\.git\b": "Git repository",
            r"\.svn\b": "SVN repository",
            r"\.DS_Store\b": "macOS metadata",
            r"wp-config\.php": "WordPress config",
        }

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        if response_status == 200:
            for pattern, desc in self.backup_indicators.items():
                if re.search(pattern, response_body):
                    return True, 0.7, f"Backup/exposed file: {desc} content detected"

            if any(ext in payload.lower() for ext in self.backup_extensions):
                content_type = response_headers.get("Content-Type", "")
                if len(response_body) > 100 and "text/html" not in content_type:
                    return True, 0.8, f"Backup file accessible at: {payload}"

        return False, 0.0, None


class VersionDisclosureTester(BaseTester):
    """Tester for Version Disclosure"""

    def __init__(self):
        super().__init__()
        self.name = "version_disclosure"
        self.version_patterns = {
            r"Server:\s*[A-Za-z0-9/-]+\s*([\d.]+)": "Server version",
            r"X-Powered-By:\s*([A-Za-z0-9/]+)": "Framework version",
            r"(?:Apache|Nginx|IIS)/([\d.]+)": "Web server version",
            r"(?:PHP|Python|Ruby|Node)/([\d.]+)": "Runtime version",
            r"(?:Django|Rails|Laravel|Express)/([\d.]+)": "Framework version",
            r"(?:WordPress|Drupal|Joomla)/([\d.]+)": "CMS version",
            r"(?:OpenSSL|TLS)\s*([\d.]+)": "SSL/TLS version",
        }

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        versions_found = []

        for header_name in ["Server", "X-Powered-By", "X-Version", "X-AspNet-Version"]:
            if header_name in response_headers:
                versions_found.append(f"{header_name}: {response_headers[header_name]}")

        for pattern, description in self.version_patterns.items():
            match = re.search(pattern, response_body)
            if match:
                versions_found.append(f"{description}: {match.group(1)}")

        if versions_found:
            return True, 0.6, f"Version disclosure: {'; '.join(versions_found[:3])}"

        return False, 0.0, None
