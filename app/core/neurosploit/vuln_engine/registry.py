import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

VULN_KNOWLEDGE_PATH = Path("/workspace/data/vuln_knowledge_base.json")


@dataclass
class VulnTypeInfo:
    key: str
    name: str
    category: str
    severity: str
    description: str
    risk_score: float
    owasp: str
    cwe_id: str
    ai_decision_prompt: str = ""
    proof_checks: List[str] = field(default_factory=list)
    payload_category: str = ""
    test_methods: List[str] = field(default_factory=list)
    remediation: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class VulnerabilityRegistry:

    ALL_TYPES = [
        "sqli_error", "sqli_union", "sqli_blind", "sqli_time",
        "xss_reflected", "xss_stored", "xss_dom", "blind_xss",
        "ssrf", "ssrf_cloud",
        "command_injection", "rce",
        "ssti",
        "lfi", "rfi", "path_traversal",
        "xxe",
        "insecure_deserialization",
        "auth_bypass",
        "jwt_manipulation",
        "csrf",
        "idor", "bola", "bfla",
        "privilege_escalation",
        "cors_misconfig",
        "open_redirect",
        "file_upload",
        "nosql_injection",
        "ldap_injection",
        "crlf_injection", "header_injection",
        "host_header_injection",
        "xml_external_entity",
        "email_injection",
        "template_injection",
        "xpath_injection",
        "ldap_injection_advanced",
        "smtp_injection",
        "code_injection",
        "eval_injection",
        "prototype_pollution",
        "http_request_smuggling",
        "http_response_splitting",
        "cache_poisoning",
        "race_condition",
        "mass_assignment",
        "excessive_data_exposure",
        "security_misconfiguration",
        "broken_authentication",
        "broken_access_control",
        "api_abuse",
        "webhook_injection",
        "graphql_injection",
        "soap_injection",
        "oauth_misconfiguration",
        "saml_vulnerability",
        "session_fixation",
        "session_hijacking",
        "clickjacking",
        "dns_rebinding",
        "tabnabbing",
        "dom_clobbering",
        "postmessage_vulnerability",
        "websocket_hijacking",
        "css_injection",
        "pdf_injection",
        "image_tragic",
        "zip_bomb",
        "xml_bomb",
        "regular_expression_dos",
        "memory_corruption",
        "buffer_overflow",
        "format_string",
        "integer_overflow",
        "heap_spray",
        "use_after_free",
        "double_free",
        "null_pointer_deref",
        "race_condition_toctou",
        "symlink_attack",
        "path_canonicalization",
        "unicode_normalization",
        "homograph_attack",
        "typosquatting",
        "dependency_confusion",
        "supply_chain_attack",
        "ci_cd_poisoning",
        "container_escape",
        "kubernetes_misconfiguration",
        "iam_privilege_escalation",
        "server_side_request_forgery_blind",
        "out_of_band_sqli",
        "out_of_band_xss",
        "blind_ssti",
        "blind_xxe",
        "blind_ssrf",
        "blind_ldap",
        "time_based_nosql",
        "error_based_nosql",
        "boolean_based_blind_sqli",
        "union_based_sqli_advanced",
        "stacked_queries_sqli",
        "second_order_sqli",
        "wide_byte_injection",
        "unicode_sqli",
        "parameter_pollution",
        "cookie_injection",
        "referer_injection",
        "user_agent_injection",
        "accept_language_injection",
        "content_type_injection",
        "multipart_injection",
        "json_injection",
        "xml_injection",
        "yaml_injection",
        "csv_injection",
        "formula_injection",
        "server_side_template_injection",
        "client_side_template_injection",
        "expression_language_injection",
        "object_injection",
        "php_object_injection",
        "python_pickle_injection",
        "java_deserialization",
        "ruby_deserialization",
        "dotnet_deserialization",
    ]

    SEVERITY_MAP = {
        "critical": {"sqli_error", "sqli_union", "sqli_blind", "sqli_time",
                     "command_injection", "rce", "auth_bypass", "ssrf", "ssrf_cloud",
                     "ssti", "insecure_deserialization", "lfi", "rfi", "xxe",
                     "xml_external_entity", "code_injection", "eval_injection"},
        "high": {"xss_reflected", "xss_stored", "xss_dom", "blind_xss",
                 "csrf", "idor", "bola", "bfla", "privilege_escalation",
                 "path_traversal", "cors_misconfig", "open_redirect",
                 "file_upload", "nosql_injection", "ldap_injection",
                 "crlf_injection", "header_injection", "host_header_injection",
                 "jwt_manipulation", "broken_authentication", "broken_access_control",
                 "second_order_sqli", "out_of_band_sqli", "stacked_queries_sqli"},
        "medium": {"email_injection", "template_injection", "xpath_injection",
                   "http_response_splitting", "cache_poisoning", "race_condition",
                   "mass_assignment", "excessive_data_exposure", "security_misconfiguration",
                   "clickjacking", "tabnabbing", "dom_clobbering",
                   "postmessage_vulnerability", "websocket_hijacking", "css_injection",
                   "session_fixation", "session_hijacking", "api_abuse",
                   "oauth_misconfiguration", "saml_vulnerability", "prototype_pollution"},
        "low": {"dns_rebinding", "homograph_attack", "typosquatting",
                "dependency_confusion", "pdf_injection", "image_tragic",
                "cookie_injection", "referer_injection", "user_agent_injection",
                "accept_language_injection", "content_type_injection",
                "multipart_injection", "json_injection", "xml_injection",
                "yaml_injection", "csv_injection", "formula_injection"},
    }

    CATEGORY_MAP = {
        "injection": {"sqli_error", "sqli_union", "sqli_blind", "sqli_time",
                      "command_injection", "rce", "nosql_injection", "ldap_injection",
                      "ldap_injection_advanced", "xpath_injection", "email_injection",
                      "code_injection", "eval_injection", "second_order_sqli",
                      "stacked_queries_sqli", "wide_byte_injection", "unicode_sqli",
                      "boolean_based_blind_sqli", "union_based_sqli_advanced",
                      "out_of_band_sqli", "time_based_nosql", "error_based_nosql",
                      "parameter_pollution", "cookie_injection", "referer_injection",
                      "user_agent_injection", "accept_language_injection",
                      "content_type_injection", "multipart_injection",
                      "json_injection", "xml_injection", "yaml_injection",
                      "csv_injection", "formula_injection", "graphql_injection",
                      "soap_injection", "smtp_injection"},
        "xss": {"xss_reflected", "xss_stored", "xss_dom", "blind_xss",
                "out_of_band_xss", "dom_clobbering", "css_injection",
                "postmessage_vulnerability"},
        "file_related": {"lfi", "rfi", "path_traversal", "file_upload",
                         "image_tragic", "zip_bomb"},
        "server_side": {"ssrf", "ssrf_cloud", "ssti", "blind_ssti", "blind_ssrf",
                        "server_side_template_injection", "webhook_injection",
                        "server_side_request_forgery_blind"},
        "auth_related": {"auth_bypass", "jwt_manipulation", "broken_authentication",
                         "session_fixation", "session_hijacking",
                         "oauth_misconfiguration", "saml_vulnerability",
                         "broken_access_control"},
        "access_control": {"idor", "bola", "bfla", "privilege_escalation",
                           "mass_assignment", "excessive_data_exposure", "api_abuse"},
        "xxe": {"xxe", "xml_external_entity", "blind_xxe", "xml_bomb", "xml_injection"},
        "deserialization": {"insecure_deserialization", "object_injection",
                            "php_object_injection", "python_pickle_injection",
                            "java_deserialization", "ruby_deserialization",
                            "dotnet_deserialization"},
        "config_related": {"cors_misconfig", "open_redirect", "security_misconfiguration",
                           "clickjacking", "host_header_injection",
                           "kubernetes_misconfiguration", "iam_privilege_escalation"},
        "header_related": {"crlf_injection", "header_injection",
                           "http_request_smuggling", "http_response_splitting",
                           "cache_poisoning"},
        "race_related": {"race_condition", "race_condition_toctou", "supply_chain_attack",
                         "ci_cd_poisoning", "dependency_confusion"},
        "memory_related": {"memory_corruption", "buffer_overflow", "format_string",
                           "integer_overflow", "heap_spray", "use_after_free",
                           "double_free", "null_pointer_deref"},
        "advanced": {"prototype_pollution", "tabnabbing", "dns_rebinding",
                     "homograph_attack", "typosquatting", "container_escape",
                     "regular_expression_dos", "symlink_attack",
                     "path_canonicalization", "unicode_normalization",
                     "pdf_injection", "expression_language_injection",
                     "client_side_template_injection", "template_injection",
                     "websocket_hijacking"},
    }

    def __init__(self):
        self._vulns: Dict[str, VulnTypeInfo] = {}
        self._loaded = False

    def load(self, knowledge_path: Optional[Path] = None) -> int:
        path = knowledge_path or VULN_KNOWLEDGE_PATH
        count = 0
        if path.exists():
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                for key, info in data.items():
                    self.register(VulnTypeInfo(
                        key=key,
                        name=info.get("name", key),
                        category=info.get("category", self._infer_category(key)),
                        severity=info.get("severity", self._infer_severity(key)),
                        description=info.get("description", ""),
                        risk_score=float(info.get("risk_score", self._infer_risk(key))),
                        owasp=info.get("owasp", ""),
                        cwe_id=info.get("cwe_id", ""),
                        ai_decision_prompt=info.get("ai_decision_prompt", ""),
                        proof_checks=info.get("proof_checks", []),
                        payload_category=info.get("payload_category", ""),
                        test_methods=info.get("test_methods", []),
                        remediation=info.get("remediation", ""),
                        metadata=info.get("metadata", {}),
                    ))
                    count += 1
                logger.info(f"VulnerabilityRegistry: loaded {count} types from {path}")
            except Exception as e:
                logger.error(f"Failed to load vuln knowledge: {e}")
        self._add_builtin_types()
        self._loaded = True
        logger.info(f"VulnerabilityRegistry: total {len(self._vulns)} types registered")
        return len(self._vulns)

    def register(self, vuln: VulnTypeInfo):
        self._vulns[vuln.key] = vuln

    def get(self, key: str) -> Optional[VulnTypeInfo]:
        return self._vulns.get(key)

    def get_by_category(self, category: str) -> List[VulnTypeInfo]:
        return [v for v in self._vulns.values() if v.category == category]

    def get_by_severity(self, severity: str) -> List[VulnTypeInfo]:
        return [v for v in self._vulns.values() if v.severity == severity]

    def get_critical_types(self) -> List[str]:
        return list(self.SEVERITY_MAP.get("critical", set()))

    def get_high_types(self) -> List[str]:
        return list(self.SEVERITY_MAP.get("high", set()))

    def all_keys(self) -> List[str]:
        return list(self._vulns.keys())

    def all_types(self) -> List[VulnTypeInfo]:
        return list(self._vulns.values())

    def has(self, key: str) -> bool:
        return key in self._vulns

    def count(self) -> int:
        return len(self._vulns)

    def _add_builtin_types(self):
        for key in self.ALL_TYPES:
            if key not in self._vulns:
                self.register(VulnTypeInfo(
                    key=key,
                    name=key.replace("_", " ").title(),
                    category=self._infer_category(key),
                    severity=self._infer_severity(key),
                    description=f"Vulnerability type: {key}",
                    risk_score=self._infer_risk(key),
                    owasp=self._infer_owasp(key),
                    cwe_id=self._infer_cwe(key),
                ))

    def _infer_category(self, key: str) -> str:
        for cat, keys in self.CATEGORY_MAP.items():
            if key in keys:
                return cat
        return "injection"

    def _infer_severity(self, key: str) -> str:
        for sev, keys in self.SEVERITY_MAP.items():
            if key in keys:
                return sev
        return "medium"

    def _infer_risk(self, key: str) -> float:
        sev = self._infer_severity(key)
        return {"critical": 10.0, "high": 7.5, "medium": 5.0, "low": 2.5}.get(sev, 5.0)

    def _infer_owasp(self, key: str) -> str:
        cat = self._infer_category(key)
        if cat in ("injection", "xxe", "server_side"):
            return "A03:2021 - Injection"
        elif cat in ("auth_related",):
            return "A07:2021 - Identification and Authentication Failures"
        elif cat in ("access_control",):
            return "A01:2021 - Broken Access Control"
        elif cat in ("xss",):
            return "A03:2021 - Injection"
        elif cat in ("deserialization",):
            return "A08:2021 - Software and Data Integrity Failures"
        elif cat in ("config_related", "header_related", "file_related"):
            return "A05:2021 - Security Misconfiguration"
        return "A03:2021 - Injection"

    def _infer_cwe(self, key: str) -> str:
        mapping = {
            "sqli_error": "CWE-89", "sqli_union": "CWE-89", "sqli_blind": "CWE-89", "sqli_time": "CWE-89",
            "xss_reflected": "CWE-79", "xss_stored": "CWE-79", "xss_dom": "CWE-79", "blind_xss": "CWE-79",
            "ssrf": "CWE-918", "ssrf_cloud": "CWE-918",
            "command_injection": "CWE-78", "rce": "CWE-94",
            "ssti": "CWE-94",
            "lfi": "CWE-98", "rfi": "CWE-98", "path_traversal": "CWE-22",
            "xxe": "CWE-611", "xml_external_entity": "CWE-611",
            "insecure_deserialization": "CWE-502",
            "auth_bypass": "CWE-287",
            "jwt_manipulation": "CWE-345",
            "csrf": "CWE-352",
            "idor": "CWE-639", "bola": "CWE-639", "bfla": "CWE-284",
            "privilege_escalation": "CWE-269",
            "cors_misconfig": "CWE-942",
            "open_redirect": "CWE-601",
            "file_upload": "CWE-434",
            "nosql_injection": "CWE-943",
            "ldap_injection": "CWE-90",
            "crlf_injection": "CWE-93",
            "header_injection": "CWE-93",
            "host_header_injection": "CWE-676",
        }
        return mapping.get(key, "CWE-74")