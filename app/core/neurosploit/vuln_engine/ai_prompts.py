import json
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class AIVulnPromptBuilder:

    VULN_DECISION_PROMPTS: Dict[str, str] = {
        "sqli_error": """Analyze the following HTTP response for SQL injection (error-based) indicators:

Response body: {body}

Payload sent: {payload}

Look for: SQL error messages, database stack traces, syntax errors, DBMS-specific error patterns (MySQL, PostgreSQL, Oracle, MSSQL).
Respond with JSON: {{"detected": true/false, "evidence": "...", "dbms": "...", "confidence": 0-100}}""",

        "sqli_union": """Analyze the following HTTP response for UNION-based SQL injection indicators:

Response body: {body}

Payload sent: {payload}

Look for: Additional data rows, column data appearing in response, structured data that wasn't in the baseline.
Respond with JSON: {{"detected": true/false, "evidence": "...", "columns_detected": N, "confidence": 0-100}}""",

        "sqli_blind": """Analyze the following HTTP response for blind SQL injection indicators:

Response body: {body}

Payload sent: {payload}

Signals observed: {signals}

Look for: Differences from baseline response (content length, status code, response content) that indicate boolean-based condition evaluation.
Respond with JSON: {{"detected": true/false, "diff_from_baseline": "...", "confidence": 0-100}}""",

        "sqli_time": """Analyze the following HTTP response for time-based SQL injection indicators:

Response time: {response_time}s
Payload sent: {payload}

Look for: Response delays of 5+ seconds that correlate with SLEEP/WAITFOR payload, indicating query execution delay.
Respond with JSON: {{"detected": true/false, "delay_seconds": N, "confidence": 0-100}}""",

        "xss_reflected": """Analyze the following HTTP response for reflected XSS indicators:

Response body: {body}

Payload sent: {payload}

Look for: Payload reflected in HTML/JS context, unescaped angle brackets, script tags in response, event handlers.
Respond with JSON: {{"detected": true/false, "context": "html/js/attribute/url", "encoding": "none/partial/encoded", "exploitable": true/false, "confidence": 0-100}}""",

        "xss_stored": """Analyze the following HTTP response for stored XSS indicators:

Response body: {body}

Payload sent: {payload}

Look for: Payload persisted and returned on subsequent page loads, appearing in data rendered to other users.
Respond with JSON: {{"detected": true/false, "persistence_confirmed": true/false, "confidence": 0-100}}""",

        "xss_dom": """Analyze the following response for DOM-based XSS indicators:

Response body: {body}

Payload sent: {payload}

Look for: JavaScript that processes URL parameters, hash fragments, or DOM data in a way that could lead to DOM XSS via document.write, innerHTML, eval, or similar sinks.
Respond with JSON: {{"detected": true/false, "sink_type": "...", "confidence": 0-100}}""",

        "ssrf": """Analyze the following HTTP response for Server-Side Request Forgery indicators:

Response body: {body}

Payload sent: {payload}

Look for: Responses from internal services (127.0.0.1, 169.254.169.254, internal IPs), cloud metadata, internal service fingerprints, timing differences for internal vs external URLs.
Respond with JSON: {{"detected": true/false, "target_reachable": "...", "data_exposed": "...", "confidence": 0-100}}""",

        "command_injection": """Analyze the following HTTP response for OS command injection indicators:

Response body: {body}

Payload sent: {payload}

Look for: Command output in response (ls, cat, id, whoami output), system file contents, execution confirmation.
Respond with JSON: {{"detected": true/false, "command_output": "...", "confidence": 0-100}}""",

        "ssti": """Analyze the following HTTP response for Server-Side Template Injection indicators:

Response body: {body}

Payload sent: {payload}

Look for: Template evaluation results (e.g., 49 from 7*7), template object attributes exposed, framework-specific error messages.
Respond with JSON: {{"detected": true/false, "framework": "...", "evaluation_result": "...", "confidence": 0-100}}""",

        "lfi": """Analyze the following HTTP response for Local File Inclusion indicators:

Response body: {body}

Payload sent: {payload}

Look for: File contents (e.g., /etc/passwd lines), base64-encoded file content, file path information disclosure.
Respond with JSON: {{"detected": true/false, "file_exposed": "...", "confidence": 0-100}}""",

        "xxe": """Analyze the following HTTP response for XML External Entity injection indicators:

Response body: {body}

Payload sent: {payload}

Look for: File contents from SYSTEM entity, error messages revealing XML parser, out-of-band data, entity expansion results.
Respond with JSON: {{"detected": true/false, "evidence": "...", "confidence": 0-100}}""",

        "csrf": """Analyze the following for CSRF vulnerability indicators:

Response body: {body}

Action performed with payload: {payload}

Look for: Missing anti-CSRF tokens, token not validated, state-changing action executed without proper CSRF protection.
Respond with JSON: {{"detected": true/false, "token_status": "...", "confidence": 0-100}}""",

        "idor": """Analyze the following HTTP response for Insecure Direct Object Reference indicators:

Response body: {body}

Payload sent: {payload}

Look for: Data accessible by changing object ID, unauthorized access to other users' resources, missing authorization checks.
Respond with JSON: {{"detected": true/false, "data_exposed": "...", "confidence": 0-100}}""",

        "auth_bypass": """Analyze the following HTTP response for authentication bypass indicators:

Response body: {body}

Payload sent: {payload}

Look for: Successful login without valid credentials, admin access gained, authentication check circumvented.
Respond with JSON: {{"detected": true/false, "bypass_method": "...", "access_level": "...", "confidence": 0-100}}""",

        "file_upload": """Analyze the following HTTP response for unsafe file upload indicators:

Response body: {body}

Filename sent: {payload}

Look for: Dangerous file extension accepted, file accessible via URL, file executed on server, MIME type bypass.
Respond with JSON: {{"detected": true/false, "upload_path": "...", "executable": true/false, "confidence": 0-100}}""",

        "open_redirect": """Analyze the following HTTP response for Open Redirect indicators:

Response body: {body}
Payload sent: {payload}

Look for: HTTP 3xx redirect to external domain, Location header pointing to attacker-controlled URL.
Respond with JSON: {{"detected": true/false, "redirect_target": "...", "confidence": 0-100}}""",

        "jwt_manipulation": """Analyze the following HTTP response for JWT manipulation indicators:

Response body: {body}

JWT sent: {payload}

Look for: Token accepted with alg:none, modified claims processed, algorithm confusion successful.
Respond with JSON: {{"detected": true/false, "manipulation_type": "...", "confidence": 0-100}}""",

        "nosql_injection": """Analyze the following HTTP response for NoSQL injection indicators:

Response body: {body}

Payload sent: {payload}

Look for: Query operator processed ($ne, $gt, $regex), unexpected data returned, authentication bypass via NoSQL operators.
Respond with JSON: {{"detected": true/false, "operator_executed": "...", "confidence": 0-100}}""",

        "insecure_deserialization": """Analyze the following HTTP response for insecure deserialization indicators:

Response body: {body}

Payload sent: {payload}

Look for: Deserialized object properties in response, execution effects, class instantiation confirmation, error messages revealing deserialization.
Respond with JSON: {{"detected": true/false, "evidence": "...", "confidence": 0-100}}""",

        "cors_misconfig": """Analyze the following HTTP response for CORS misconfiguration indicators:

Response headers: {headers}
Response body: {body}

Look for: Access-Control-Allow-Origin: null, wildcard origin, credentials with wildcard origin, overly permissive CORS policy.
Respond with JSON: {{"detected": true/false, "misconfig_type": "...", "confidence": 0-100}}""",

        "privilege_escalation": """Analyze the following HTTP response for privilege escalation indicators:

Response body: {body}

Payload sent: {payload}

Look for: Elevated access granted, admin functions accessible, role manipulation successful.
Respond with JSON: {{"detected": true/false, "new_privilege": "...", "confidence": 0-100}}""",

        "path_traversal": """Analyze the following HTTP response for path traversal indicators:

Response body: {body}

Payload sent: {payload}

Look for: File contents from outside web root, directory listing, system files exposed.
Respond with JSON: {{"detected": true/false, "file_accessed": "...", "confidence": 0-100}}""",

        "prototype_pollution": """Analyze the following HTTP response for prototype pollution indicators:

Response body: {body}

Payload sent: {payload}

Look for: Object properties modified globally, isAdmin/constructor/__proto__ pollution effects, application behavior changes.
Respond with JSON: {{"detected": true/false, "polluted_property": "...", "confidence": 0-100}}""",
    }

    def build_decision_prompt(self, vuln_type: str, body: str, payload: str, signals: List[str], **kwargs) -> str:
        template = self.VULN_DECISION_PROMPTS.get(vuln_type, self._generic_prompt(vuln_type))
        try:
            return template.format(
                body=body[:3000],
                payload=payload[:500],
                signals=", ".join(signals),
                response_time=kwargs.get("response_time", "N/A"),
                headers=kwargs.get("headers", "N/A"),
            )
        except KeyError:
            return self._generic_prompt(vuln_type).format(
                body=body[:3000], payload=payload[:500], signals=", ".join(signals)
            )

    def _generic_prompt(self, vuln_type: str) -> str:
        return f"""Analyze the following HTTP response for {vuln_type} indicators:

Response body: {{body}}

Payload sent: {{payload}}

Signals observed: {{signals}}

Look for any evidence of {vuln_type} exploitation success.
Respond with JSON: {{"detected": true/false, "evidence": "...", "confidence": 0-100}}"""

    def build_analysis_prompt(self, finding: Dict[str, Any]) -> str:
        return f"""Provide a detailed security analysis for this finding:

Vulnerability Type: {finding.get('vuln_type', 'Unknown')}
Target URL: {finding.get('url', 'Unknown')}
Parameter: {finding.get('param', 'Unknown')}
Severity: {finding.get('severity', 'Unknown')}
Confidence Score: {finding.get('confidence_score', 0)}/100
Proof Type: {finding.get('proof_type', 'Unknown')}
Evidence: {finding.get('evidence', '')[:1000]}

Provide:
1. Technical description of the vulnerability
2. Impact assessment
3. Exploitation scenario
4. Remediation steps
5. References (CWE, OWASP)"""

    def build_summary_prompt(self, findings: List[Dict]) -> str:
        return f"""Summarize the following security scan results:

Total findings: {len(findings)}
Findings:
{json.dumps(findings[:10], indent=2)}

Provide:
1. Executive summary
2. Risk overview
3. Top 5 most critical findings
4. Recommended immediate actions
5. Overall security posture assessment"""