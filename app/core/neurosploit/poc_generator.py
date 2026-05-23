"""
PoC Generator - generates Proof of Concept payloads for discovered vulnerabilities.

Creates browser-executable HTML PoCs, curl commands, Python scripts,
and detailed exploitation scenarios for each validated finding.
"""

import re
import json
import base64
import urllib.parse
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class PoCFormat(Enum):
    HTML = "html"             # Browser-openable HTML PoC
    CURL = "curl"             # Single curl command
    PYTHON = "python"         # Python requests script
    BASH = "bash"             # Bash script with curl
    MARKDOWN = "markdown"     # Markdown report (for LLM integration)
    RAW = "raw"               # Raw payload


class VulnCategory(Enum):
    XSS = "xss"
    SQLI = "sqli"
    SSTI = "ssti"
    SSRF = "ssrf"
    RCE = "rce"
    LFI = "lfi"
    PATH_TRAVERSAL = "path_traversal"
    FILE_UPLOAD = "file_upload"
    IDOR = "idor"
    CSRF = "csrf"
    XXE = "xxe"
    COMMAND_INJECTION = "command_injection"
    OPEN_REDIRECT = "open_redirect"
    DESERIALIZATION = "deserialization"
    NOSQL_INJECTION = "nosql_injection"
    LDAP_INJECTION = "ldap_injection"
    XPATH_INJECTION = "xpath_injection"
    CRLF_INJECTION = "crlf_injection"
    HOST_HEADER = "host_header"
    CORS = "cors"
    CACHE_POISONING = "cache_poisoning"
    PROTOTYPE_POLLUTION = "prototype_pollution"
    INFORMATION_DISCLOSURE = "information_disclosure"
    MISCONFIGURATION = "misconfiguration"
    SESSION_FIXATION = "session_fixation"
    UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class PoCRequest:
    """Single HTTP request for a PoC."""
    method: str = "GET"
    url: str = ""
    headers: Dict[str, str] = field(default_factory=dict)
    data: str = ""
    params: Dict[str, str] = field(default_factory=dict)
    cookies: Dict[str, str] = field(default_factory=dict)
    json_body: Optional[Dict] = None


@dataclass
class PoCArtifact:
    """Generated PoC artifact."""
    finding_id: str = ""
    category: str = ""
    title: str = ""
    description: str = ""
    format: str = "html"
    content: str = ""
    curl_command: str = ""
    python_script: str = ""
    markdown_report: str = ""
    steps_to_reproduce: List[str] = field(default_factory=list)
    severity: str = "high"
    cvss_score: float = 7.5
    cvss_vector: str = ""
    cwe_id: str = ""
    remediation: str = ""
    references: List[str] = field(default_factory=list)
    raw_payload: str = ""
    target_info: Dict[str, str] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# HTML PoC Templates
# ---------------------------------------------------------------------------

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PoC: {title} — NeuroSploit</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: #0d1117;
            color: #c9d1d9;
            padding: 2rem;
            max-width: 900px;
            margin: 0 auto;
        }}
        .header {{
            background: linear-gradient(135deg, #1a365d, #161b22);
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        .header h1 {{ font-size: 1.5rem; color: #e6edf3; }}
        .header .meta {{
            margin-top: 0.75rem;
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            font-size: 0.85rem;
            color: #8b949e;
        }}
        .header .meta span {{
            background: #21262d;
            border: 1px solid #30363d;
            border-radius: 4px;
            padding: 0.2rem 0.6rem;
        }}
        .severity-critical {{ background: #da3633 !important; color: #fff !important; }}
        .severity-high    {{ background: #f85149 !important; color: #fff !important; }}
        .severity-medium  {{ background: #d29922 !important; color: #000 !important; }}
        .severity-low     {{ background: #238636 !important; color: #fff !important; }}
        .severity-info    {{ background: #58a6ff !important; color: #fff !important; }}

        .section {{
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        }}
        .section h2 {{
            font-size: 1.1rem;
            color: #58a6ff;
            margin-bottom: 0.75rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #21262d;
        }}

        pre {{
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 4px;
            padding: 0.75rem;
            overflow-x: auto;
            font-family: 'Cascadia Code', 'Fira Code', monospace;
            font-size: 0.8rem;
            color: #e6edf3;
            margin: 0.5rem 0;
        }}

        .exploit-btn {{
            background: linear-gradient(135deg, #da3633, #f85149);
            color: #fff;
            border: none;
            border-radius: 6px;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.2s;
            margin-top: 1rem;
        }}
        .exploit-btn:hover {{
            transform: scale(1.02);
            box-shadow: 0 0 20px rgba(248, 81, 73, 0.3);
        }}

        .ref-list {{ list-style: none; }}
        .ref-list li {{ padding: 0.25rem 0; font-size: 0.85rem; }}
        .ref-list li a {{ color: #58a6ff; text-decoration: none; }}
        .ref-list li a:hover {{ text-decoration: underline; }}

        .step-list li {{ padding: 0.3rem 0; }}
    </style>
</head>
<body>

<div class="header">
    <h1>PoC: {title}</h1>
    <div class="meta">
        <span>Category: {category}</span>
        <span class="severity-{severity}">Severity: {severity}</span>
        <span>CVSS: {cvss_score}</span>
        <span>CWE: {cwe_id}</span>
        <span>Target: {target_url}</span>
    </div>
</div>

<div class="section">
    <h2>Description</h2>
    <p>{description}</p>
</div>

<div class="section">
    <h2>Steps to Reproduce</h2>
    <ol class="step-list">
        {steps_html}
    </ol>
</div>

<div class="section">
    <h2>Exploit</h2>
    <p>Click the button below to execute the PoC:</p>
    {exploit_html}
    <div id="poc-result" style="margin-top:1rem;"></div>
</div>

<div class="section">
    <h2>cURL Command</h2>
    <pre><code>{curl_command}</code></pre>
</div>

<div class="section">
    <h2>Remediation</h2>
    <p>{remediation}</p>
</div>

<div class="section">
    <h2>References</h2>
    <ul class="ref-list">
        {references_html}
    </ul>
</div>

{auto_exec_script}

</body>
</html>"""


# ---------------------------------------------------------------------------
# PoC Generator
# ---------------------------------------------------------------------------

class PoCGenerator:
    """Generates PoC content for vulnerabilities discovered by NeuroSploit."""

    # Vulnerability category -> CWE mapping
    CATEGORY_CWE = {
        "sqli": "CWE-89",
        "xss": "CWE-79",
        "lfi": "CWE-22",
        "rce": "CWE-77",
        "ssti": "CWE-1336",
        "ssrf": "CWE-918",
        "open_redirect": "CWE-601",
        "idor": "CWE-639",
        "csrf": "CWE-352",
        "xxe": "CWE-611",
        "command_injection": "CWE-77",
        "nosql_injection": "CWE-943",
        "deserialization": "CWE-502",
        "ldap_injection": "CWE-90",
        "xpath_injection": "CWE-643",
        "crlf_injection": "CWE-93",
        "host_header": "CWE-441",
        "cors": "CWE-942",
        "path_traversal": "CWE-23",
        "file_upload": "CWE-434",
        "session_fixation": "CWE-384",
        "information_disclosure": "CWE-200",
        "misconfiguration": "CWE-16",
        "prototype_pollution": "CWE-1321",
    }

    # Severity -> CVSS score range
    SEVERITY_CVSS = {
        "critical": (9.0, 10.0),
        "high": (7.0, 8.9),
        "medium": (4.0, 6.9),
        "low": (0.1, 3.9),
        "info": (0.0, 0.0),
    }

    def generate_html_poc(self, finding: Dict) -> PoCArtifact:
        """Generate an HTML PoC file for a vulnerability finding."""
        title = finding.get("title", finding.get("vulnerability", "XSS Vulnerability"))
        category = finding.get("category", finding.get("type", "xss")).lower()
        severity = finding.get("severity", "high").lower()
        description = finding.get("description", "A cross-site scripting vulnerability was discovered.")
        curl_cmd = finding.get("curl_command", self._generate_curl(finding))
        target_url = finding.get("target", finding.get("url", "N/A"))
        steps = finding.get("steps_to_reproduce", [])
        exploit_html = finding.get("exploit_html", "")
        remediation = finding.get("remediation", "")
        references = finding.get("references", [])
        cvss = finding.get("cvss_score", self._default_cvss(severity))
        cwe_id = finding.get("cwe_id", self.CATEGORY_CWE.get(category, "CWE-79"))
        finding_id = finding.get("id", "")

        if not steps:
            steps = self._auto_generate_steps(finding)

        if not exploit_html:
            exploit_html = self._generate_exploit_html(finding)

        if not remediation:
            remediation = self._generate_remediation(category)

        if not references:
            references = self._generate_references(category)

        # Auto-exec script for immediate XSS
        auto_exec = ""
        if category == "xss" and severity in ("critical", "high"):
            auto_exec = self._generate_auto_exec_script(finding)

        steps_html = "\n".join(f"<li>{step}</li>" for step in steps)
        refs_html = "\n".join(
            f"<li><a href=\"{ref}\" target=\"_blank\">{ref}</a></li>" if ref.startswith("http") else f"<li>{ref}</li>"
            for ref in references
        )

        content = HTML_TEMPLATE.format(
            title=html_escape(title),
            category=html_escape(category.upper()),
            severity=html_escape(severity),
            cvss_score=f"{cvss:.1f}",
            cwe_id=html_escape(cwe_id),
            target_url=html_escape(target_url),
            description=html_escape(description),
            steps_html=steps_html,
            exploit_html=exploit_html,
            curl_command=html_escape(curl_cmd),
            remediation=html_escape(remediation),
            references_html=refs_html,
            auto_exec_script=auto_exec,
        )

        return PoCArtifact(
            finding_id=finding_id,
            category=category,
            title=title,
            description=description,
            format="html",
            content=content,
            curl_command=curl_cmd,
            markdown_report=self._generate_markdown(finding),
            steps_to_reproduce=steps,
            severity=severity,
            cvss_score=cvss,
            cvss_vector=finding.get("cvss_vector", ""),
            cwe_id=cwe_id,
            remediation=remediation,
            references=references,
            raw_payload=finding.get("payload", finding.get("value", "")),
            target_info={
                "url": target_url,
                "parameter": finding.get("parameter", finding.get("param", "")),
                "method": finding.get("method", "GET"),
            },
        )

    def generate_curl_poc(self, finding: Dict) -> str:
        """Generate a single curl command for reproducing the vulnerability."""
        method = finding.get("method", "GET").upper()
        url = finding.get("url", finding.get("target", ""))
        headers = finding.get("headers", {})
        body = finding.get("body", finding.get("data", ""))
        cookies = finding.get("cookies", {})
        payload = finding.get("payload", finding.get("value", ""))

        cmd_parts = ["curl"]

        if method != "GET":
            cmd_parts.append(f"-X {method}")

        # Headers
        for k, v in headers.items():
            cmd_parts.append(f'-H "{k}: {v}"')

        # Cookies
        if cookies:
            cookie_str = "; ".join(f"{k}={v}" for k, v in cookies.items())
            cmd_parts.append(f'-b "{cookie_str}"')

        # Body
        if body:
            cmd_parts.append(f'-d "{body}"')

        # URL
        cmd_parts.append(f'"{url}"')

        return " \\\n  ".join(cmd_parts)

    def generate_python_poc(self, finding: Dict) -> str:
        """Generate a Python requests script for the PoC."""
        method = finding.get("method", "GET").upper()
        url = finding.get("url", finding.get("target", ""))
        headers = finding.get("headers", {})
        body = finding.get("body", finding.get("data", ""))
        params = finding.get("params", {})
        cookies = finding.get("cookies", {})
        payload = finding.get("payload", finding.get("value", ""))

        lines = [
            "#!/usr/bin/env python3",
            '"""PoC script for XSS vulnerability"""',
            "",
            "import requests",
            "",
            "url = \"{}\"".format(url),
            "",
            "headers = {",
        ]
        for k, v in headers.items():
            lines.append(f'    "{k}": "{v}",')
        lines.append("}")

        if params:
            lines.append("params = {")
            for k, v in params.items():
                lines.append(f'    "{k}": "{v}",')
            lines.append("}")

        if cookies:
            lines.append("cookies = {")
            for k, v in cookies.items():
                lines.append(f'    "{k}": "{v}",')
            lines.append("}")

        lines.append("")
        req_args = ["url", "headers=headers"]
        if params:
            req_args.append("params=params")
        if cookies:
            req_args.append("cookies=cookies")
        if body:
            lines.append(f'data = "{body}"')
            req_args.append("data=data")

        method_map = {"GET": "requests.get", "POST": "requests.post",
                      "PUT": "requests.put", "DELETE": "requests.delete",
                      "PATCH": "requests.patch"}

        lines.append(f"response = {method_map.get(method, 'requests.get')}({', '.join(req_args)})")
        lines.append("print(f'Status: {response.status_code}')")
        lines.append("print(f'Response: {response.text[:500]}')")

        return "\n".join(lines)

    def generate_bash_poc(self, finding: Dict) -> str:
        """Generate a bash script with curl."""
        curl_cmd = self.generate_curl_poc(finding)
        lines = [
            "#!/bin/bash",
            "# PoC Exploit Script",
            f"# Target: {finding.get('target', finding.get('url', 'N/A'))}",
            f"# Vulnerability: {finding.get('title', 'XSS')}",
            f"# Severity: {finding.get('severity', 'high').upper()}",
            "",
            curl_cmd,
        ]
        return "\n".join(lines)

    def generate_markdown(self, finding: Dict) -> str:
        """Generate a Markdown report for the finding."""
        title = finding.get("title", "XSS Vulnerability")
        category = finding.get("category", finding.get("type", "xss")).upper()
        severity = finding.get("severity", "high").upper()
        description = finding.get("description", "XSS vulnerability found.")
        target_url = finding.get("target", finding.get("url", "N/A"))
        steps = finding.get("steps_to_reproduce", [])
        curl_cmd = finding.get("curl_command", self._generate_curl(finding))
        impact = finding.get("impact", "")
        remediation = finding.get("remediation", "")

        lines = [
            f"# Finding: {title}",
            "",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| **Category** | {category} |",
            f"| **Severity** | {severity} |",
            f"| **Target** | `{target_url}` |",
            f"| **CVSS Score** | {finding.get('cvss_score', 7.5)} |",
            f"| **CWE** | {finding.get('cwe_id', 'CWE-79')} |",
            "",
            "## Description",
            "",
            description,
            "",
            "## Steps to Reproduce",
            "",
        ]

        for i, step in enumerate(steps or ["1. Navigate to target", "2. Inject payload", "3. Observe XSS execution"], 1):
            lines.append(f"{i}. {step}")

        lines.extend([
            "",
            "## Proof of Concept",
            "",
            "```bash",
            curl_cmd,
            "```",
            "",
        ])

        if impact:
            lines.extend([
                "## Impact",
                "",
                impact,
                "",
            ])

        if remediation:
            lines.extend([
                "## Remediation",
                "",
                remediation,
                "",
            ])

        return "\n".join(lines)

    def generate_batch(self, findings: List[Dict]) -> List[PoCArtifact]:
        """Generate PoCs for multiple findings."""
        poc_list = []
        for f in findings:
            poc = self.generate_html_poc(f)
            poc_list.append(poc)
        return poc_list

    # ── Private Helpers ────────────────────────────────────────────────

    def _generate_curl(self, finding: Dict) -> str:
        """Build a curl command from finding data."""
        method = finding.get("method", "GET").upper()
        url = finding.get("url", finding.get("target", "http://EXAMPLE/"))
        payload = finding.get("payload", finding.get("value", "<script>alert(1)</script>"))

        parts = ["curl"]
        if method != "GET":
            parts.append(f"-X {method}")

        # URL-encode the payload if it's in a parameter
        param = finding.get("parameter", finding.get("param", ""))
        if param and payload:
            encoded = urllib.parse.quote(payload, safe="")
            # Replace the payload in the URL if present
            if payload in url:
                test_url = url.replace(payload, encoded)
                parts.append(f'"{test_url}"')
            else:
                parts.append(f'"{url}"')
        else:
            parts.append(f'"{url}"')

        return " \\\n  ".join(parts)

    def _generate_exploit_html(self, finding: Dict) -> str:
        """Generate exploit button / form HTML."""
        category = (finding.get("category") or finding.get("type") or "xss").lower()
        payload = finding.get("payload", finding.get("value", "alert(1)"))
        target_url = finding.get("target", finding.get("url", ""))

        if category == "xss":
            return (
                f'<button class="exploit-btn" onclick="{payload}">'
                f'Execute XSS Payload</button>'
            )
        elif category == "open_redirect":
            return (
                f'<button class="exploit-btn" onclick="'
                f"window.location.href='{target_url}'\">"
                f'Trigger Open Redirect</button>'
            )
        elif category == "sqli":
            return (
                f'<p>SQL Injection detected. Use the cURL command below to '
                f'reproduce the injection and extract database contents.</p>'
            )
        else:
            return (
                f'<button class="exploit-btn" onclick="'
                f"fetch('{target_url}').then(r=>r.text()).then(t=>"
                f"document.getElementById('poc-result').innerText=t)"
                f'">Send Exploit Request</button>'
            )

    def _generate_auto_exec_script(self, finding: Dict) -> str:
        """Generate auto-exec script that fires XSS on page load."""
        payload = finding.get("payload", finding.get("value", "alert(document.cookie)"))
        return f"""
<script>
(function() {{
    try {{
        setTimeout(function() {{
            {payload};
        }}, 500);
    }} catch(e) {{ console.error('PoC auto-exec failed:', e); }}
}})();
</script>
"""

    def _auto_generate_steps(self, finding: Dict) -> List[str]:
        """Generate reproduction steps if not provided."""
        category = (finding.get("category") or finding.get("type") or "xss").lower()
        target_url = finding.get("target", finding.get("url", "the target application"))
        param = finding.get("parameter", finding.get("param", "input"))

        template_steps = {
            "xss": [
                f"Navigate to {target_url}",
                f"Inject the XSS payload into the '{param}' parameter",
                "Submit the request",
                "Observe that the injected JavaScript executes in the victim's browser",
            ],
            "sqli": [
                f"Navigate to {target_url}",
                f"Inject the SQL injection payload into the '{param}' parameter",
                "Submit the request",
                "Observe database error or extracted data indicating successful injection",
            ],
            "ssrf": [
                f"Send a request to {target_url}",
                f"Modify the '{param}' parameter to point to an attacker-controlled server",
                "Submit the request",
                "Verify the target server makes a request to the controlled server",
            ],
            "lfi": [
                f"Navigate to {target_url}",
                f"Inject the path traversal payload into the '{param}' parameter",
                "Submit the request",
                "Observe the contents of the targeted file in the response",
            ],
            "open_redirect": [
                f"Navigate to {target_url}",
                f"Add the redirect payload to the '{param}' parameter",
                "Execute the request",
                "Observe that the application redirects to the attacker-controlled destination",
            ],
        }

        generic = [
            f"Navigate to the vulnerable endpoint at {target_url}",
            f"Submit the crafted payload via the '{param}' parameter",
            "Observe the application behavior confirming the vulnerability",
        ]

        return template_steps.get(category, generic)

    def _generate_remediation(self, category: str) -> str:
        """Generate category-specific remediation advice."""
        remediations = {
            "xss": (
                "1. Implement context-aware output encoding for all user-controlled data."
                " 2. Use Content-Security-Policy headers with strict script-src directives."
                " 3. Validate and sanitize all input on the server side."
                " 4. Use modern frameworks that auto-escape by default (React, Angular, Vue)."
            ),
            "sqli": (
                "1. Use parameterized queries / prepared statements 100% of the time."
                " 2. Implement an ORM that handles escaping automatically."
                " 3. Apply least-privilege database user permissions."
                " 4. Deploy a Web Application Firewall (WAF) as a secondary defense."
            ),
            "ssrf": (
                "1. Implement a strict allow-list of permitted URLs/IPs for outbound requests."
                " 2. Block requests to internal/private IP ranges (10.x, 172.16-31.x, 192.168.x, 127.x)."
                " 3. Disable HTTP redirect following in server-side requests."
                " 4. Use a dedicated proxy with network-level egress filtering."
            ),
            "lfi": (
                "1. Avoid passing user input to filesystem functions (include, require, fopen)."
                " 2. If dynamic file inclusion is required, use a strict whitelist of allowed files."
                " 3. Sanitize input to reject path traversal sequences (../, ..\\\\)."
                " 4. Configure open_basedir / equivalent to restrict filesystem access."
            ),
            "open_redirect": (
                "1. Use a whitelist of allowed redirect destinations."
                " 2. Use relative paths or internal identifiers instead of user-supplied URLs."
                " 3. Validate that redirect URLs belong to the same domain."
                " 4. Display an intermediate warning page before external redirects."
            ),
            "rce": (
                "1. NEVER pass user input to system command execution functions."
                " 2. Use safe APIs instead of shell execution (e.g., subprocess with args list)."
                " 3. Run application processes with minimal privileges."
                " 4. Deploy a WAF and runtime application self-protection (RASP)."
            ),
        }

        if category in remediations:
            return remediations[category]

        return (
            "1. Implement proper input validation on all user-controllable parameters."
            " 2. Apply the principle of least privilege throughout the application."
            " 3. Conduct regular security testing to identify new vulnerabilities."
            " 4. Keep all frameworks, libraries, and dependencies up-to-date."
        )

    def _generate_references(self, category: str) -> List[str]:
        """Generate relevant references for the vulnerability category."""
        refs = {
            "xss": [
                "https://owasp.org/www-community/attacks/xss/",
                "https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html",
                "https://portswigger.net/web-security/cross-site-scripting",
                "https://cwe.mitre.org/data/definitions/79.html",
            ],
            "sqli": [
                "https://owasp.org/www-community/attacks/SQL_Injection",
                "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html",
                "https://portswigger.net/web-security/sql-injection",
                "https://cwe.mitre.org/data/definitions/89.html",
            ],
            "ssrf": [
                "https://owasp.org/www-community/attacks/Server_Side_Request_Forgery",
                "https://portswigger.net/web-security/ssrf",
                "https://cwe.mitre.org/data/definitions/918.html",
            ],
            "lfi": [
                "https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11.1-Testing_for_Local_File_Inclusion",
                "https://cwe.mitre.org/data/definitions/22.html",
            ],
            "open_redirect": [
                "https://owasp.org/www-community/attacks/Unvalidated_Redirects_and_Forwards",
                "https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html",
                "https://cwe.mitre.org/data/definitions/601.html",
            ],
        }

        return refs.get(category, ["https://owasp.org/www-project-web-security-testing-guide/"])

    @staticmethod
    def _default_cvss(severity: str) -> float:
        """Return default CVSS score for a severity level."""
        cvss_map = {
            "critical": 9.0,
            "high": 7.5,
            "medium": 5.0,
            "low": 2.5,
            "info": 0.0,
        }
        return cvss_map.get(severity.lower(), 5.0)


# ---------------------------------------------------------------------------
# HTML escape helper
# ---------------------------------------------------------------------------

def html_escape(text: str) -> str:
    """Escape HTML special characters."""
    if not text:
        return ""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )