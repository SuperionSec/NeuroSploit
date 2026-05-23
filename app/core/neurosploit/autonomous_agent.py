"""
NeuroSploit v3 - Autonomous Security Agent

AI-Powered Autonomous Security Agent with 3-stream parallel architecture:
  Stream 1 (Recon) ──→ asyncio.Queue ──→ Stream 2 (Junior Pentester)
  Stream 3 (Tool Runner) using HTTP-based tools (graceful degradation, no Docker)
  All streams feed findings in real-time via callbacks.

AUTHORIZATION: This is an authorized penetration testing tool.
All actions are performed with explicit permission.
"""

import asyncio
import aiohttp
import hashlib
import json
import logging
import os
import random
import re
import subprocess
import sys
import time
import traceback
from collections import defaultdict, OrderedDict
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, quote

logger = logging.getLogger(__name__)

# ── LLM Libraries ──
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    anthropic = None

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None

# ── Core Module Imports ──
try:
    from app.core.neurosploit.agent_memory import AgentMemory
    HAS_MEMORY = True
except ImportError:
    HAS_MEMORY = False
    AgentMemory = None

try:
    from app.core.neurosploit.vuln_registry import VulnerabilityRegistry
    HAS_VULN_REGISTRY = True
except ImportError:
    HAS_VULN_REGISTRY = False
    VulnerabilityRegistry = None

try:
    from app.core.neurosploit.payload_generator import PayloadGenerator
    HAS_PAYLOAD_GEN = True
except ImportError:
    HAS_PAYLOAD_GEN = False
    PayloadGenerator = None

try:
    from app.core.neurosploit.response_verifier import ResponseVerifier
    HAS_RESP_VERIFIER = True
except ImportError:
    HAS_RESP_VERIFIER = False
    ResponseVerifier = None

try:
    from app.core.neurosploit.chain_engine import ChainEngine
    HAS_CHAIN = True
except ImportError:
    HAS_CHAIN = False
    ChainEngine = None

try:
    from app.core.neurosploit.validation_judge import ValidationJudge, NegativeControlEngine, ProofOfExecution, ConfidenceScorer
    HAS_VALIDATION = True
except ImportError:
    HAS_VALIDATION = False
    ValidationJudge = None
    NegativeControlEngine = None
    ProofOfExecution = None
    ConfidenceScorer = None

try:
    from app.core.neurosploit.access_control import AccessControlLearner
    HAS_AC_LEARNER = True
except ImportError:
    HAS_AC_LEARNER = False
    AccessControlLearner = None

try:
    from app.core.neurosploit.token_budget import TokenBudget
    HAS_TOKEN_BUDGET = True
except ImportError:
    HAS_TOKEN_BUDGET = False
    TokenBudget = None

try:
    from app.core.neurosploit.reasoning_engine import ReasoningEngine
    HAS_REASONING = True
except ImportError:
    HAS_REASONING = False
    ReasoningEngine = None

try:
    from app.core.neurosploit.agent_tasks import AgentTaskManager
    HAS_AGENT_TASKS = True
except ImportError:
    HAS_AGENT_TASKS = False
    AgentTaskManager = None

try:
    from app.core.neurosploit.endpoint_classifier import EndpointClassifier
    HAS_ENDPOINT_CLASSIFIER = True
except ImportError:
    HAS_ENDPOINT_CLASSIFIER = False
    EndpointClassifier = None

try:
    from app.core.neurosploit.banner_analyzer import BannerAnalyzer
    HAS_BANNER_ANALYZER = True
except ImportError:
    HAS_BANNER_ANALYZER = False
    BannerAnalyzer = None

try:
    from app.core.neurosploit.payload_mutator import PayloadMutator
    HAS_PAYLOAD_MUTATOR = True
except ImportError:
    HAS_PAYLOAD_MUTATOR = False
    PayloadMutator = None

try:
    from app.core.neurosploit.param_analyzer import ParameterAnalyzer
    HAS_PARAM_ANALYZER = True
except ImportError:
    HAS_PARAM_ANALYZER = False
    ParameterAnalyzer = None

try:
    from app.core.neurosploit.xss_validator import XSSValidator
    HAS_XSS_VALIDATOR = True
except ImportError:
    HAS_XSS_VALIDATOR = False
    XSSValidator = None

try:
    from app.core.neurosploit.request_repeater import RequestRepeater
    HAS_REQUEST_REPEATER = True
except ImportError:
    HAS_REQUEST_REPEATER = False
    RequestRepeater = None

try:
    from app.core.neurosploit.site_analyzer import SiteAnalyzer
    HAS_SITE_ANALYZER = True
except ImportError:
    HAS_SITE_ANALYZER = False
    SiteAnalyzer = None

try:
    from app.core.neurosploit.exploit_generator import ExploitGenerator
    HAS_EXPLOIT_GENERATOR = True
except ImportError:
    HAS_EXPLOIT_GENERATOR = False
    ExploitGenerator = None

try:
    from app.core.neurosploit.poc_validator import PoCValidator
    HAS_POC_VALIDATOR = True
except ImportError:
    HAS_POC_VALIDATOR = False
    PoCValidator = None

try:
    from app.core.neurosploit.adaptive_learner import AdaptiveLearner
    HAS_ADAPTIVE_LEARNER = True
except ImportError:
    HAS_ADAPTIVE_LEARNER = False
    AdaptiveLearner = None

try:
    from app.core.neurosploit.rag import RAGEngine, FewShotSelector, ReasoningMemory
    HAS_RAG = True
except ImportError:
    HAS_RAG = False
    RAGEngine = None
    FewShotSelector = None
    ReasoningMemory = None

try:
    from app.core.neurosploit.pentest_playbook import (
        get_playbook_entry, get_testing_prompts, get_bypass_strategies,
        get_verification_checklist, build_agent_testing_prompt,
        get_anti_fp_rules, get_chain_attacks, get_playbook_summary,
    )
    HAS_PLAYBOOK = True
except ImportError:
    HAS_PLAYBOOK = False

try:
    from app.core.neurosploit.scope_manager import ScopeManager
    HAS_SCOPE = True
except ImportError:
    HAS_SCOPE = False
    ScopeManager = None

try:
    from app.core.neurosploit.checkpoint_manager import CheckpointManager
    HAS_CHECKPOINT = True
except ImportError:
    HAS_CHECKPOINT = False
    CheckpointManager = None

try:
    from app.core.neurosploit.smart_router import get_router, SmartRouter
    HAS_SMART_ROUTER = True
except ImportError:
    HAS_SMART_ROUTER = False
    get_router = None

try:
    from app.core.neurosploit.agent_orchestrator import AgentOrchestrator
    HAS_ORCHESTRATOR = True
except ImportError:
    HAS_ORCHESTRATOR = False
    AgentOrchestrator = None

try:
    from app.core.neurosploit.researcher_agent import ResearcherAgent
    HAS_RESEARCHER = True
except ImportError:
    HAS_RESEARCHER = False
    ResearcherAgent = None

try:
    from app.core.neurosploit.vuln_agent_orchestrator import VulnAgentOrchestrator
    HAS_VULN_AGENTS = True
except ImportError:
    HAS_VULN_AGENTS = False
    VulnAgentOrchestrator = None


class OperationMode(Enum):
    RECON_ONLY = "recon_only"
    FULL_AUTO = "full_auto"
    PROMPT_ONLY = "prompt_only"
    ANALYZE_ONLY = "analyze_only"
    AUTO_PENTEST = "auto_pentest"
    CLI_AGENT = "cli_agent"
    FULL_LLM_PENTEST = "full_llm_pentest"


class FindingSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class CVSSScore:
    score: float
    severity: str
    vector: str


@dataclass
class Finding:
    id: str = ""
    title: str = ""
    severity: str = "medium"
    vulnerability_type: str = ""
    cvss_score: float = 0.0
    cvss_vector: str = ""
    cwe_id: str = ""
    description: str = ""
    affected_endpoint: str = ""
    parameter: str = ""
    payload: str = ""
    evidence: str = ""
    request: str = ""
    response: str = ""
    impact: str = ""
    poc_code: str = ""
    remediation: str = ""
    references: List[str] = field(default_factory=list)
    screenshots: List[str] = field(default_factory=list)
    affected_urls: List[str] = field(default_factory=list)
    ai_verified: bool = False
    confidence: str = "0"
    confidence_score: int = 0
    confidence_breakdown: Dict = field(default_factory=dict)
    proof_of_execution: str = ""
    negative_controls: str = ""
    ai_status: str = "confirmed"
    rejection_reason: str = ""
    double_checked: bool = False
    evidence_request: str = ""
    evidence_response: str = ""


@dataclass
class ReconData:
    subdomains: List[str] = field(default_factory=list)
    live_hosts: List[str] = field(default_factory=list)
    endpoints: List[Dict] = field(default_factory=list)
    parameters: Dict[str, List[str]] = field(default_factory=dict)
    technologies: List[str] = field(default_factory=list)
    forms: List[Dict] = field(default_factory=list)
    js_files: List[str] = field(default_factory=list)
    api_endpoints: List[str] = field(default_factory=list)


def _get_endpoint_url(ep) -> str:
    if isinstance(ep, str):
        return ep
    elif isinstance(ep, dict):
        return ep.get("url", "")
    return ""


def _get_endpoint_method(ep) -> str:
    if isinstance(ep, dict):
        return ep.get("method", "GET")
    return "GET"


class LLMClient:
    """Unified LLM client for Claude, OpenAI, Ollama, and Gemini"""

    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    LMSTUDIO_URL = os.getenv("LMSTUDIO_URL", "http://localhost:1234")
    GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta"

    def __init__(self, preferred_provider: Optional[str] = None, preferred_model: Optional[str] = None):
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.google_key = os.getenv("GOOGLE_API_KEY", "") or os.getenv("GEMINI_API_KEY", "")
        self.together_key = os.getenv("TOGETHER_API_KEY", "")
        self.fireworks_key = os.getenv("FIREWORKS_API_KEY", "")
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
        self.codex_key = os.getenv("CODEX_API_KEY", "")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")
        self.configured_model = os.getenv("DEFAULT_LLM_MODEL", "")
        self.client = None
        self.provider = None
        self.model_name = None
        self.error_message = None
        self.connection_tested = False
        self._smart_router = None
        self._preferred_provider = preferred_provider
        self._preferred_model = preferred_model

        if HAS_SMART_ROUTER and get_router:
            router = get_router()
            if router:
                self._smart_router = router
                self.provider = "smart_router"
                self.client = "smart_router"
                if preferred_provider and preferred_model:
                    self.model_name = f"{preferred_provider}/{preferred_model}"
                elif preferred_model:
                    self.model_name = preferred_model
                elif preferred_provider:
                    self.model_name = f"{preferred_provider} (auto)"
                else:
                    self.model_name = "auto"
                return

        if self.anthropic_key in ["", "your-anthropic-api-key"]:
            self.anthropic_key = None
        if self.openai_key in ["", "your-openai-api-key"]:
            self.openai_key = None
        if self.google_key in ["", "your-google-api-key"]:
            self.google_key = None
        if self.together_key in ["", "your-together-api-key"]:
            self.together_key = None
        if self.fireworks_key in ["", "your-fireworks-api-key"]:
            self.fireworks_key = None
        if self.openrouter_key in ["", "your-openrouter-api-key"]:
            self.openrouter_key = None
        if self.codex_key in ["", "your-codex-api-key"]:
            self.codex_key = None

        self._initialize_provider()

    def _initialize_provider(self):
        if ANTHROPIC_AVAILABLE and self.anthropic_key:
            try:
                self.client = anthropic.Anthropic(api_key=self.anthropic_key)
                self.provider = "claude"
                self.model_name = self.configured_model or "claude-sonnet-4-20250514"
                return
            except Exception as e:
                self.error_message = f"Claude init error: {e}"

        if OPENAI_AVAILABLE and self.openai_key:
            try:
                self.client = openai.OpenAI(api_key=self.openai_key)
                self.provider = "openai"
                self.model_name = self.configured_model or "gpt-4o"
                return
            except Exception as e:
                self.error_message = f"OpenAI init error: {e}"

        if OPENAI_AVAILABLE and self.codex_key:
            try:
                self.client = openai.OpenAI(api_key=self.codex_key)
                self.provider = "codex"
                self.model_name = self.configured_model or "codex-mini-latest"
                return
            except Exception as e:
                self.error_message = f"Codex init error: {e}"

        if self.google_key:
            self.client = "gemini"
            self.provider = "gemini"
            self.model_name = self.configured_model or "gemini-pro"
            return

        if self.openrouter_key:
            self.client = "openrouter"
            self.provider = "openrouter"
            self.model_name = self.configured_model or "anthropic/claude-sonnet-4-20250514"
            return

        if self.together_key:
            self.client = "together"
            self.provider = "together"
            self.model_name = self.configured_model or "meta-llama/Llama-3.3-70B-Instruct-Turbo"
            return

        if self.fireworks_key:
            self.client = "fireworks"
            self.provider = "fireworks"
            self.model_name = self.configured_model or "accounts/fireworks/models/llama-v3p3-70b-instruct"
            return

        if self._check_ollama():
            self.client = "ollama"
            self.provider = "ollama"
            self.model_name = self.configured_model or self.ollama_model
            return

        if self._check_lmstudio():
            self.client = "lmstudio"
            self.provider = "lmstudio"
            self.model_name = self.configured_model or ""
            return

        self._set_no_provider_error()

    def _check_ollama(self) -> bool:
        try:
            import requests
            response = requests.get(f"{self.OLLAMA_URL}/api/tags", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def _check_lmstudio(self) -> bool:
        try:
            import requests
            response = requests.get(f"{self.LMSTUDIO_URL}/v1/models", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def _set_no_provider_error(self):
        errors = []
        if not ANTHROPIC_AVAILABLE and not OPENAI_AVAILABLE:
            errors.append("LLM libraries not installed (run: pip install anthropic openai)")
        all_keys = [self.anthropic_key, self.openai_key, self.google_key,
                     self.openrouter_key, self.together_key, self.fireworks_key, self.codex_key]
        if not any(all_keys):
            errors.append("No API keys configured")
        if not self._check_ollama():
            errors.append("Ollama not running locally")
        if not self._check_lmstudio():
            errors.append("LM Studio not running locally")
        self.error_message = "No LLM provider available. " + "; ".join(errors)

    def is_available(self) -> bool:
        return self.client is not None or self._smart_router is not None

    def get_status(self) -> dict:
        status = {
            "available": self.is_available(),
            "provider": self.provider,
            "model": self.model_name,
            "error": self.error_message,
            "anthropic_lib": ANTHROPIC_AVAILABLE,
            "openai_lib": OPENAI_AVAILABLE,
            "ollama_available": self._check_ollama(),
            "lmstudio_available": self._check_lmstudio(),
            "has_google_key": bool(self.google_key),
            "smart_router_enabled": self._smart_router is not None,
        }
        if self._smart_router:
            status["smart_router_status"] = self._smart_router.get_status()
        return status

    async def test_connection(self) -> Tuple[bool, str]:
        if not self.client:
            return False, self.error_message or "No LLM client configured"
        try:
            result = await self.generate("Say 'OK' if you can hear me.", max_tokens=10)
            if result:
                self.connection_tested = True
                return True, f"Connected to {self.provider}"
            return False, f"Empty response from {self.provider}"
        except Exception as e:
            return False, f"Connection test failed for {self.provider}: {str(e)}"

    async def generate(self, prompt: str, system: str = "", max_tokens: int = 4096) -> str:
        if not self.client:
            raise LLMConnectionError(self.error_message or "No LLM provider available")

        default_system = "You are an expert penetration tester and security researcher."

        if self._smart_router:
            try:
                result = await self._smart_router.generate(
                    prompt=prompt, system=system or default_system,
                    max_tokens=max_tokens,
                    preferred_provider=self._preferred_provider,
                    model=self._preferred_model,
                )
                return result
            except Exception as e:
                if not self.anthropic_key and not self.openai_key and not self.google_key:
                    raise LLMConnectionError(f"SmartRouter failed and no direct provider: {e}")

        try:
            if self.provider == "claude":
                message = self.client.messages.create(
                    model=self.model_name or "claude-sonnet-4-20250514",
                    max_tokens=max_tokens,
                    system=system or default_system,
                    messages=[{"role": "user", "content": prompt}]
                )
                return message.content[0].text

            elif self.provider in ("openai", "codex"):
                response = self.client.chat.completions.create(
                    model=self.model_name or ("gpt-4o" if self.provider == "openai" else "codex-mini-latest"),
                    max_tokens=max_tokens,
                    messages=[
                        {"role": "system", "content": system or default_system},
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.choices[0].message.content

            elif self.provider == "gemini":
                return await self._generate_gemini(prompt, system or default_system, max_tokens)

            elif self.provider == "openrouter":
                return await self._generate_openai_compatible(
                    prompt, system or default_system, max_tokens,
                    url="https://openrouter.ai/api/v1/chat/completions",
                    api_key=self.openrouter_key,
                    model=self.model_name or "anthropic/claude-sonnet-4-20250514",
                    extra_headers={"HTTP-Referer": "https://neurosploit.ai", "X-Title": "NeuroSploit"},
                )

            elif self.provider in ("together", "fireworks"):
                url = "https://api.together.xyz/v1/chat/completions" if self.provider == "together" else "https://api.fireworks.ai/inference/v1/chat/completions"
                key = self.together_key if self.provider == "together" else self.fireworks_key
                return await self._generate_openai_compatible(
                    prompt, system or default_system, max_tokens,
                    url=url, api_key=key, model=self.model_name,
                )

            elif self.provider == "ollama":
                return await self._generate_ollama(prompt, system or default_system)

            elif self.provider == "lmstudio":
                return await self._generate_lmstudio(prompt, system or default_system, max_tokens)

        except LLMConnectionError:
            raise
        except Exception as e:
            raise LLMConnectionError(f"API call failed ({self.provider}): {str(e)}")

        return ""

    async def _generate_openai_compatible(self, prompt, system, max_tokens, url, api_key, model, extra_headers=None):
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        if extra_headers:
            headers.update(extra_headers)

        payload = {"model": model, "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ], "max_tokens": max_tokens}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers,
                                     timeout=aiohttp.ClientTimeout(total=120)) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise LLMConnectionError(f"API error ({response.status}): {error_text[:500]}")
                data = await response.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "")

    async def _generate_gemini(self, prompt, system, max_tokens):
        gemini_model = self.model_name or "gemini-pro"
        url = f"{self.GEMINI_URL}/models/{gemini_model}:generateContent?key={self.google_key}"
        payload = {"contents": [{"parts": [{"text": f"{system}\n\n{prompt}"}]}],
                    "generationConfig": {"maxOutputTokens": max_tokens}}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=60)) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise LLMConnectionError(f"Gemini API error ({response.status}): {error_text}")
                data = await response.json()
                return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

    async def _generate_ollama(self, prompt, system):
        url = f"{self.OLLAMA_URL}/api/generate"
        payload = {"model": self.model_name or self.ollama_model, "prompt": prompt, "system": system, "stream": False}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=120)) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise LLMConnectionError(f"Ollama error ({response.status}): {error_text}")
                data = await response.json()
                return data.get("response", "")

    async def _generate_lmstudio(self, prompt, system, max_tokens):
        url = f"{self.LMSTUDIO_URL}/v1/chat/completions"
        payload = {"messages": [{"role": "system", "content": system},
                                {"role": "user", "content": prompt}],
                    "max_tokens": max_tokens, "stream": False}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=120)) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise LLMConnectionError(f"LM Studio error ({response.status}): {error_text}")
                data = await response.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "")


class LLMConnectionError(Exception):
    pass


DEFAULT_ASSESSMENT_PROMPT = """You are NeuroSploit, an elite autonomous penetration testing AI agent.
Your mission: identify real, exploitable vulnerabilities — zero false positives.

## METHODOLOGY (PTES/OWASP/WSTG aligned)

### Phase 1 — Reconnaissance & Fingerprinting
- Discover all endpoints, parameters, forms, API paths, WebSocket URLs
- Technology fingerprinting: language, framework, server, WAF, CDN
- Identify attack surface: file upload, auth endpoints, admin panels, GraphQL

### Phase 2 — Technology-Guided Prioritization
Select vulnerability types based on detected technology stack:
- PHP/Laravel → LFI, command injection, SSTI (Blade), SQLi, file upload
- Node.js/Express → NoSQL injection, SSRF, prototype pollution, SSTI (EJS/Pug)
- Python/Django/Flask → SSTI (Jinja2), command injection, IDOR, mass assignment
- Java/Spring → XXE, insecure deserialization, expression language injection, SSRF
- ASP.NET → path traversal, XXE, header injection, insecure deserialization
- API/REST → IDOR, BOLA, BFLA, JWT manipulation, mass assignment, rate limiting
- GraphQL → introspection, injection, DoS via nested queries

### Phase 3 — Active Testing
**OWASP Top 10 2021 coverage:**
- A01 Broken Access Control: IDOR, BOLA, BFLA, privilege escalation, forced browsing, CORS
- A02 Cryptographic Failures: weak encryption/hashing, cleartext transmission, SSL issues
- A03 Injection: SQLi, NoSQL, LDAP, XPath, command, SSTI, XSS, XXE
- A04 Insecure Design: business logic, race condition, mass assignment
- A05 Security Misconfiguration: headers, debug mode, directory listing, default creds
- A06 Vulnerable Components: outdated dependencies
- A07 Auth Failures: JWT, session fixation, brute force, 2FA bypass, OAuth misconfig
- A08 Data Integrity: insecure deserialization, cache poisoning, HTTP smuggling
- A10 SSRF: standard SSRF, cloud metadata SSRF

### Phase 4 — Verification (multi-signal)
Every finding MUST have:
1. Concrete HTTP evidence (request + response)
2. At least 2 verification signals OR high-confidence tester match
3. No speculative language — only confirmed exploitable issues

## CRITICAL RULES
- NEVER report theoretical/speculative vulnerabilities
- ALWAYS verify with real HTTP evidence before confirming
- Test systematically: every parameter, every endpoint, every form
- Use technology hints to select the most relevant tests
"""


class AutonomousAgent:
    """
    AI-Powered Autonomous Security Agent
    3-stream parallel architecture with HTTP-based tool execution.
    No Docker/Kali sandbox — tools run natively or are gracefully skipped.
    """

    VULN_TYPE_MAP = {
        "sqli": "sqli_error", "xss": "xss_reflected", "rce": "command_injection",
        "cors": "cors_misconfig", "lfi_rfi": "lfi", "file_inclusion": "lfi",
        "remote_code_execution": "command_injection", "broken_auth": "auth_bypass",
        "broken_access": "bola", "api_abuse": "rest_api_versioning",
        "sqli_error": "sqli_error", "sqli_union": "sqli_union",
        "sqli_blind": "sqli_blind", "sqli_time": "sqli_time",
        "command_injection": "command_injection", "ssti": "ssti",
        "nosql_injection": "nosql_injection", "ldap_injection": "ldap_injection",
        "xpath_injection": "xpath_injection", "graphql_injection": "graphql_injection",
        "crlf_injection": "crlf_injection", "header_injection": "header_injection",
        "email_injection": "email_injection", "expression_language_injection": "expression_language_injection",
        "log_injection": "log_injection", "html_injection": "html_injection",
        "csv_injection": "csv_injection", "orm_injection": "orm_injection",
        "xss_reflected": "xss_reflected", "xss_stored": "xss_stored",
        "xss_dom": "xss_dom", "blind_xss": "blind_xss", "mutation_xss": "mutation_xss",
        "lfi": "lfi", "rfi": "rfi", "path_traversal": "path_traversal",
        "xxe": "xxe", "file_upload": "file_upload",
        "arbitrary_file_read": "arbitrary_file_read", "arbitrary_file_delete": "arbitrary_file_delete",
        "zip_slip": "zip_slip",
        "ssrf": "ssrf", "ssrf_cloud": "ssrf_cloud",
        "csrf": "csrf", "cors_misconfig": "cors_misconfig",
        "auth_bypass": "auth_bypass", "jwt_manipulation": "jwt_manipulation",
        "session_fixation": "session_fixation", "weak_password": "weak_password",
        "default_credentials": "default_credentials", "brute_force": "brute_force",
        "two_factor_bypass": "two_factor_bypass", "oauth_misconfiguration": "oauth_misconfiguration",
        "idor": "idor", "bola": "bola", "bfla": "bfla",
        "privilege_escalation": "privilege_escalation",
        "mass_assignment": "mass_assignment", "forced_browsing": "forced_browsing",
        "clickjacking": "clickjacking", "open_redirect": "open_redirect",
        "dom_clobbering": "dom_clobbering", "postmessage_vulnerability": "postmessage_vulnerability",
        "websocket_hijacking": "websocket_hijacking", "prototype_pollution": "prototype_pollution",
        "css_injection": "css_injection", "tabnabbing": "tabnabbing",
        "security_headers": "security_headers", "ssl_issues": "ssl_issues",
        "http_methods": "http_methods", "directory_listing": "directory_listing",
        "debug_mode": "debug_mode", "exposed_admin_panel": "exposed_admin_panel",
        "exposed_api_docs": "exposed_api_docs", "insecure_cookie_flags": "insecure_cookie_flags",
        "http_smuggling": "http_smuggling", "cache_poisoning": "cache_poisoning",
        "race_condition": "race_condition", "business_logic": "business_logic",
        "rate_limit_bypass": "rate_limit_bypass",
        "parameter_pollution": "parameter_pollution", "type_juggling": "type_juggling",
        "insecure_deserialization": "insecure_deserialization",
        "subdomain_takeover": "subdomain_takeover", "host_header_injection": "host_header_injection",
        "timing_attack": "timing_attack", "improper_error_handling": "improper_error_handling",
        "sensitive_data_exposure": "sensitive_data_exposure",
        "information_disclosure": "information_disclosure",
        "api_key_exposure": "api_key_exposure", "source_code_disclosure": "source_code_disclosure",
        "backup_file_exposure": "backup_file_exposure", "version_disclosure": "version_disclosure",
        "weak_encryption": "weak_encryption", "weak_hashing": "weak_hashing",
        "weak_random": "weak_random", "cleartext_transmission": "cleartext_transmission",
        "vulnerable_dependency": "vulnerable_dependency", "outdated_component": "outdated_component",
        "insecure_cdn": "insecure_cdn",
        "s3_bucket_misconfiguration": "s3_bucket_misconfiguration",
        "cloud_metadata_exposure": "cloud_metadata_exposure",
        "serverless_misconfiguration": "serverless_misconfiguration",
        "graphql_introspection": "graphql_introspection", "graphql_dos": "graphql_dos",
        "rest_api_versioning": "rest_api_versioning",
        "soap_injection": "soap_injection", "api_rate_limiting": "api_rate_limiting",
        "excessive_data_exposure": "excessive_data_exposure",
    }

    def __init__(
        self,
        target: str,
        mode: OperationMode = OperationMode.FULL_AUTO,
        log_callback: Optional[Callable] = None,
        progress_callback: Optional[Callable] = None,
        auth_headers: Optional[Dict] = None,
        task: Optional[Any] = None,
        custom_prompt: Optional[str] = None,
        recon_context: Optional[Dict] = None,
        finding_callback: Optional[Callable] = None,
        lab_context: Optional[Dict] = None,
        scan_id: Optional[str] = None,
        loaded_custom_prompts: Optional[List[Dict]] = None,
        preferred_provider: Optional[str] = None,
        preferred_model: Optional[str] = None,
        methodology_file: Optional[str] = None,
        **kwargs,
    ):
        self.target = self._normalize_target(target)
        self.mode = mode
        self.log = log_callback or self._default_log
        self.progress_callback = progress_callback
        self.finding_callback = finding_callback
        self.auth_headers = auth_headers or {}
        self.task = task
        self.custom_prompt = custom_prompt
        self.recon_context = recon_context
        self.lab_context = lab_context or {}
        self.scan_id = scan_id
        self.loaded_custom_prompts: List[Dict] = loaded_custom_prompts or []
        self.preferred_provider = preferred_provider
        self.preferred_model = preferred_model
        self._cancelled = False
        self._paused = False
        self._skip_to_phase: Optional[str] = None

        self.session: Optional[aiohttp.ClientSession] = None
        self.llm = LLMClient(
            preferred_provider=preferred_provider,
            preferred_model=preferred_model,
        )

        # VulnEngine integration
        self.vuln_registry = VulnerabilityRegistry() if HAS_VULN_REGISTRY else None
        self.payload_generator = PayloadGenerator() if HAS_PAYLOAD_GEN else None
        self.response_verifier = ResponseVerifier() if HAS_RESP_VERIFIER else None
        self.knowledge_base = self._load_knowledge_base()

        # PoC generator
        try:
            from app.core.neurosploit.poc_generator import PoCGenerator
            self.poc_generator = PoCGenerator()
        except Exception:
            self.poc_generator = None

        # Validation pipeline
        self.negative_controls = NegativeControlEngine() if HAS_VALIDATION else None
        self.proof_engine = ProofOfExecution() if HAS_VALIDATION else None
        self.confidence_scorer = ConfidenceScorer() if HAS_VALIDATION else None
        if HAS_VALIDATION:
            try:
                self.validation_judge = ValidationJudge(
                    self.negative_controls, self.proof_engine,
                    self.confidence_scorer, self.llm,
                    access_control_learner=getattr(self, 'access_control_learner', None)
                )
            except Exception:
                self.validation_judge = None
        else:
            self.validation_judge = None

        # Execution history
        try:
            from app.core.neurosploit.execution_history import ExecutionHistory
            self.execution_history = ExecutionHistory()
        except Exception:
            self.execution_history = None

        # Access control learner
        try:
            self.access_control_learner = AccessControlLearner() if HAS_AC_LEARNER else None
        except Exception:
            self.access_control_learner = None

        # Adaptive learner
        self.adaptive_learner = None
        if HAS_ADAPTIVE_LEARNER:
            try:
                self.adaptive_learner = AdaptiveLearner()
            except Exception:
                pass

        # RAG Engine
        self.rag_engine = None
        self.few_shot_selector = None
        self.reasoning_memory = None
        if HAS_RAG and os.getenv("ENABLE_RAG", "true").lower() != "false":
            try:
                rag_backend = os.getenv("RAG_BACKEND", "auto")
                self.rag_engine = RAGEngine(data_dir="data", backend=rag_backend)
                self.few_shot_selector = FewShotSelector(rag_engine=self.rag_engine)
                self.reasoning_memory = ReasoningMemory()
            except Exception:
                pass

        # Methodology loader
        self.methodology_index = None
        try:
            from app.core.neurosploit.methodology_loader import MethodologyLoader
            _meth_file = methodology_file or os.getenv("METHODOLOGY_FILE")
            if _meth_file and os.path.exists(_meth_file):
                _loader = MethodologyLoader()
                self.methodology_index = _loader.load_from_file(_meth_file)
            elif self.loaded_custom_prompts:
                _loader = MethodologyLoader()
                self.methodology_index = _loader.load_from_db_prompts(self.loaded_custom_prompts)
        except Exception:
            pass

        if self.methodology_index and self.validation_judge:
            self.validation_judge.methodology_index = self.methodology_index

        # Autonomy modules
        self.request_engine = None
        self.waf_detector = None
        self.strategy = None
        self.chain_engine = ChainEngine(llm=self.llm) if HAS_CHAIN else None
        self.auth_manager = None
        self._waf_result = None

        # Token budget + Reasoning engine
        self.token_budget = None
        if HAS_TOKEN_BUDGET and os.getenv("TOKEN_BUDGET"):
            self.token_budget = TokenBudget(total_budget=int(os.getenv("TOKEN_BUDGET", "100000")))

        self.reasoning_engine = None
        if HAS_REASONING and os.getenv("ENABLE_REASONING", "true").lower() == "true":
            self.reasoning_engine = ReasoningEngine(self.llm, self.token_budget)

        self.task_manager = AgentTaskManager() if HAS_AGENT_TASKS else None

        # Phase 2 modules
        self.endpoint_classifier = EndpointClassifier() if HAS_ENDPOINT_CLASSIFIER else None
        self.cve_hunter = None
        self.deep_recon = None
        self.banner_analyzer = BannerAnalyzer() if HAS_BANNER_ANALYZER else None

        # Phase 3 modules
        self.payload_mutator = PayloadMutator() if HAS_PAYLOAD_MUTATOR else None
        self.param_analyzer = ParameterAnalyzer() if HAS_PARAM_ANALYZER else None
        self.xss_validator = XSSValidator() if HAS_XSS_VALIDATOR else None

        # Phase 3.5 modules
        self.request_repeater = RequestRepeater() if HAS_REQUEST_REPEATER else None
        self.site_analyzer = SiteAnalyzer() if HAS_SITE_ANALYZER else None

        # Phase 4 modules
        self.exploit_generator = ExploitGenerator() if HAS_EXPLOIT_GENERATOR else None
        self.poc_validator_engine = None

        # Phase 5: Multi-agent orchestrator
        self._orchestrator = None

        # Researcher AI (0-day discovery, no sandbox)
        self._researcher = None

        # Phase 6: Vuln agent orchestrator
        self._vuln_orchestrator = None

        # CLI agent (disabled — no sandbox)
        self._cli_agent = None

        # Checkpoint persistence
        self._checkpoint_manager = (
            CheckpointManager(self.scan_id) if HAS_CHECKPOINT and self.scan_id else None
        )
        self._last_progress = 0
        self._last_phase = ""

        # Data storage
        self.recon = ReconData()
        self.memory = AgentMemory() if HAS_MEMORY else None
        self._site_architecture = None
        self.custom_prompts: List[str] = []
        self.tool_executions: List[Dict] = []
        self.rejected_findings: List[Finding] = []
        self._sandbox = None
        self.container_status: Optional[Dict] = None

        # 3-stream shared state
        self._endpoint_queue: Optional[asyncio.Queue] = None
        self._recon_complete: Optional[asyncio.Event] = None
        self._tools_complete: Optional[asyncio.Event] = None
        self._stream_findings_count: int = 0
        self._junior_tested_types: set = set()
        self._playbook_recommended_types: List[str] = []
        self._current_playbook_context: str = ""
        self._master_plan: Dict = {}

    @property
    def findings(self) -> List[Finding]:
        if self.memory:
            return self.memory.confirmed_findings
        return []

    def cancel(self):
        self._cancelled = True
        self._paused = False
        if self._vuln_orchestrator:
            self._vuln_orchestrator.cancel()

    def is_cancelled(self) -> bool:
        return self._cancelled

    def pause(self):
        self._paused = True

    def resume(self):
        self._paused = False

    def is_paused(self) -> bool:
        return self._paused

    async def _wait_if_paused(self):
        while self._paused and not self._cancelled:
            await asyncio.sleep(1)

    # ═══════════════════════ Misc utilities ═══════════════════════

    @staticmethod
    def _normalize_target(target: str) -> str:
        if not target.startswith("http"):
            target = "https://" + target
        return target.rstrip("/")

    @staticmethod
    def _load_knowledge_base() -> Dict:
        kb_path = Path(__file__).parent.parent.parent.parent / "data" / "vuln_knowledge_base.json"
        try:
            with open(kb_path) as f:
                return json.load(f)
        except Exception:
            return {}

    def _map_vuln_type(self, vuln_type: str) -> str:
        return self.VULN_TYPE_MAP.get(vuln_type, vuln_type)

    def _get_payloads(self, vuln_type: str) -> List[str]:
        if not self.payload_generator:
            return []
        mapped = self._map_vuln_type(vuln_type)
        payloads = self.payload_generator.payload_libraries.get(mapped, [])
        if not payloads:
            payloads = self.payload_generator.payload_libraries.get(vuln_type, [])
        return payloads

    def _get_request_timeout(self) -> int:
        return int(os.getenv("REQUEST_TIMEOUT", "30"))

    def _save_checkpoint(self):
        if not self._checkpoint_manager:
            return
        try:
            state = {
                "target": self.target, "mode": self.mode.value,
                "progress": self._last_progress, "phase": self._last_phase,
                "recon_data": {
                    "endpoints": [{"url": e.get("url", ""), "method": e.get("method", "GET")}
                                  for e in self.recon.endpoints[:50]],
                    "technologies": list(self.recon.technologies),
                },
                "findings": [
                    {"title": f.title, "vuln_type": f.vulnerability_type,
                     "severity": f.severity, "endpoint": f.affected_endpoint,
                     "confidence_score": getattr(f, 'confidence_score', 0)}
                    for f in self.findings
                ],
                "rejected_count": len(self.rejected_findings),
                "junior_tested_types": list(self._junior_tested_types),
            }
            self._checkpoint_manager.save(state)
        except Exception:
            pass

    async def _default_log(self, level: str, message: str):
        print(f"[{level.upper()}] {message}")

    async def log_llm(self, level: str, message: str):
        await self.log(level, message)

    async def _update_progress(self, pct: int, phase: str):
        self._last_progress = pct
        self._last_phase = phase
        if self.progress_callback:
            try:
                await self.progress_callback(pct, phase)
            except Exception:
                pass
        self._save_checkpoint()

    # ═══════════════════════ Session Management ═══════════════════════

    async def __aenter__(self):
        connector = aiohttp.TCPConnector(ssl=False, limit=50)
        timeout = aiohttp.ClientTimeout(total=self._get_request_timeout())
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        headers.update(self.auth_headers)
        self.session = aiohttp.ClientSession(connector=connector, timeout=timeout, headers=headers)

        # Lazy-init request engine
        try:
            from app.core.neurosploit.request_engine import RequestEngine
            self.request_engine = RequestEngine(self.session)
        except Exception:
            self.request_engine = self

        # Lazy-init orchestrator
        if HAS_ORCHESTRATOR and os.getenv("ENABLE_MULTI_AGENT", "").lower() == "true":
            try:
                self._orchestrator = AgentOrchestrator(
                    llm=self.llm, budget=self.token_budget,
                    request_engine=self.request_engine,
                    config={"budget_splits": {"recon": 0.20, "exploit": 0.35, "validator": 0.20, "cve_hunter": 0.10, "reporter": 0.15}},
                )
            except Exception:
                self._orchestrator = None

        # Lazy-init researcher (no sandbox)
        if HAS_RESEARCHER and os.getenv("ENABLE_RESEARCHER_AI", "").lower() == "true":
            try:
                self._researcher = ResearcherAgent(
                    llm=self.llm, scan_id=self.scan_id or "unknown",
                    target=self.target,
                    log_callback=self.log, progress_callback=self._update_progress,
                    finding_callback=self.finding_callback,
                    token_budget=self.token_budget,
                )
            except Exception:
                self._researcher = None

        return self

    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
        if self._researcher:
            await self._researcher.shutdown()

    # ═══════════════════════ Main Run Dispatch ═══════════════════════

    async def run(self) -> Dict[str, Any]:
        try:
            if self.mode == OperationMode.AUTO_PENTEST:
                return await self._run_auto_pentest()
            elif self.mode == OperationMode.CLI_AGENT:
                return await self._run_cli_agent_mode()
            elif self.mode == OperationMode.FULL_LLM_PENTEST:
                return await self._run_full_llm_pentest()
            else:
                return await self._run_full_mode()
        except Exception as e:
            traceback.print_exc()
            return self._generate_error_report(str(e))

    # ═══════════════════════ Full Mode (Recon + Analysis + Testing) ═══════════════════════

    async def _run_full_mode(self) -> Dict:
        await self._update_progress(0, "Reconnaissance starting")
        await self._run_recon()

        skip = self._check_skip("recon")
        if skip:
            await self.log("info", f"Skipping to phase: {skip}")

        await self._update_progress(30, "AI Analysis")
        attack_plan = await self._ai_analyze_attack_surface()

        await self._update_progress(50, "Vulnerability Testing")
        await self._test_all_vulnerabilities(attack_plan)

        await self._update_progress(80, "Enhancing findings")
        await self._ai_enhance_findings()

        await self._update_progress(90, "Generating report")
        report = await self._generate_full_report()
        await self._update_progress(100, "Complete")
        return report

    # ═══════════════════════ 3-STREAM AUTO PENTEST ═══════════════════════

    async def _run_auto_pentest(self) -> Dict:
        """Parallel auto pentest: 3 concurrent streams + deep analysis + report.

        Architecture:
          Stream 1 (Recon)  ──→ asyncio.Queue ──→ Stream 2 (Junior Pentester)
          Stream 3 (Tool Runner) runs HTTP-based tools (graceful degradation)
          All streams feed findings in real-time via callbacks.
        """
        await self._update_progress(0, "Auto pentest starting")
        await self.log("info", "=" * 60)
        await self.log("info", "  PARALLEL AUTO PENTEST MODE")
        await self.log("info", "  3 concurrent streams | AI-powered | 100 vuln types")
        await self.log("info", "=" * 60)

        if not self.custom_prompt:
            self.custom_prompt = DEFAULT_ASSESSMENT_PROMPT

        # Multi-agent orchestrator (if enabled)
        if self._orchestrator:
            await self.log("info", "  [MULTI-AGENT] Orchestrator enabled")
            orch_result = await self._orchestrator.run(
                target=self.target, recon_data=self.recon,
                initial_context={"headers": dict(self.auth_headers),
                                 "technologies": self.recon.technologies}
            )
            for f in orch_result.get("findings", []):
                if isinstance(f, Finding):
                    await self._add_finding(f)
            report = await self._generate_full_report()
            await self._update_progress(100, "Multi-agent pentest complete")
            if self.execution_history:
                self.execution_history.flush()
            return report

        # Shared state for parallel streams
        self._endpoint_queue = asyncio.Queue()
        self._recon_complete = asyncio.Event()
        self._tools_complete = asyncio.Event()
        self._stream_findings_count = 0
        self._junior_tested_types = set()
        self._playbook_recommended_types = []
        self._current_playbook_context = ""

        # AI master plan
        self._master_plan = {}
        if self.llm.is_available():
            try:
                await self.log("info", "[MASTER PLAN] AI strategic planning")
                master_plan = await self._ai_master_plan()
                if master_plan:
                    self._master_plan = master_plan
                    profile = master_plan.get("target_profile", "")
                    risk = master_plan.get("risk_assessment", "")
                    priority_types = master_plan.get("priority_vuln_types", [])
                    if profile:
                        await self.log("info", f"  Profile: {profile[:120]}")
                    if risk:
                        await self.log("info", f"  Risk: {risk[:120]}")
                    if priority_types:
                        await self.log("info", f"  Priority: {', '.join(priority_types[:8])}")
            except Exception as e:
                await self.log("debug", f"  Planning error: {e}")

        # ── CONCURRENT PHASE (0-50%): 3 parallel streams ──
        await asyncio.gather(
            self._stream_recon(),
            self._stream_junior_pentest(),
            self._stream_tool_runner(),
        )

        parallel_findings = len(self.findings)
        await self.log("info", f"  Parallel phase complete: {parallel_findings} findings, "
                       f"{len(self._junior_tested_types)} types pre-tested")
        await self._update_progress(50, "Parallel streams complete")

        # Reasoning checkpoint at 50%
        if self.reasoning_engine and self.llm.is_available():
            try:
                plan = await self.reasoning_engine.plan_attack(
                    recon_summary=f"{len(self.recon.endpoints)} endpoints, "
                                  f"{len(self.recon.technologies)} techs",
                    findings_so_far=self.findings,
                    tested_types=self._junior_tested_types,
                    progress_pct=0.50,
                )
                if plan and plan.priority_vulns:
                    await self.log("info", f"  [REASONING] Plan: {', '.join(plan.priority_vulns[:5])}")
                    for vtype in plan.priority_vulns:
                        if vtype not in self._junior_tested_types:
                            self._junior_tested_types.discard(vtype)
            except Exception as e:
                await self.log("debug", f"  [REASONING] Plan error: {e}")

        # ── DEEP ANALYSIS PHASE (50-75%) ──
        await self.log("info", "[DEEP] AI Attack Surface Analysis + Comprehensive Testing")
        attack_plan = await self._ai_analyze_attack_surface()

        default_plan = self._default_attack_plan()
        ai_types = attack_plan.get("priority_vulns", [])
        playbook_types = self._playbook_recommended_types[:15] if self._playbook_recommended_types else []
        all_types = default_plan["priority_vulns"]
        merged_types = list(dict.fromkeys(ai_types + playbook_types + all_types))
        remaining = [t for t in merged_types if t not in self._junior_tested_types]
        attack_plan["priority_vulns"] = remaining
        await self.log("info", f"  {len(remaining)} remaining types "
                       f"({len(self._junior_tested_types)} already tested)")
        await self._update_progress(55, "Deep: attack surface analyzed")

        await self.log("info", "[DEEP] Comprehensive Vulnerability Testing")
        await self._test_all_vulnerabilities(attack_plan)
        await self._update_progress(75, "Deep testing complete")

        # CVE hunting
        if self.cve_hunter and self.recon.technologies:
            try:
                await self.log("info", "[CVE] Searching for known CVEs")
                cve_findings = await self.cve_hunter.hunt(
                    headers=dict(self.auth_headers), body="",
                    technologies=self.recon.technologies,
                )
                for cvf in (cve_findings or []):
                    await self.log("info", f"  CVE: {getattr(cvf, 'cve_id', '?')}")
            except Exception as e:
                await self.log("debug", f"  CVE hunt error: {e}")

        # Chain discovery
        if self.chain_engine and len(self.findings) >= 2 and self.llm.is_available():
            try:
                chains = await self.chain_engine.ai_discover_chains(
                    self.findings, self.recon, self.llm, self.token_budget
                )
                if chains:
                    await self.log("info", f"  [CHAIN] {len(chains)} exploit chains discovered")
            except Exception as e:
                await self.log("debug", f"  Chain discovery error: {e}")

        # Researcher AI (graceful degradation — no sandbox)
        if self._researcher and not self.is_cancelled():
            try:
                await self.log("info", "[RESEARCHER] Starting 0-day research (HTTP-based)")
                self._researcher.recon_data = {
                    "endpoints": [{"url": ep.get("url", ""), "method": ep.get("method", "GET")}
                                  for ep in self.recon.endpoints[:50]],
                    "technologies": self.recon.technologies,
                    "parameters": self.recon.parameters,
                    "response_headers": getattr(self.recon, 'response_headers', {}),
                }
                self._researcher.existing_findings = self.findings

                ok, msg = await self._researcher.initialize()
                if ok:
                    research_result = await self._researcher.run()
                    for rf in research_result.findings:
                        finding = Finding(
                            title=rf.get("title", "Research Finding"),
                            severity=rf.get("severity", "medium"),
                            vulnerability_type=rf.get("vulnerability_type", "unknown"),
                            description=rf.get("description") or rf.get("evidence") or "",
                            affected_endpoint=rf.get("affected_endpoint", self.target),
                            evidence=rf.get("evidence", ""),
                            impact=rf.get("impact", ""),
                            poc_code=rf.get("poc_code", ""),
                            confidence_score=rf.get("confidence_score", 50),
                            confidence=("high" if rf.get("confidence_score", 0) >= 80
                                        else "medium" if rf.get("confidence_score", 0) >= 50
                                        else "low"),
                            ai_verified=True, ai_status="confirmed",
                        )
                        if self.memory:
                            self.memory.add_confirmed_finding(finding)
                else:
                    await self.log("warning", f"[RESEARCHER] Init failed: {msg}")
            except Exception as e:
                await self.log("warning", f"[RESEARCHER] Error: {e}")

        # Double-check phase
        if self.findings and not self.is_cancelled():
            await self.log("info", "[DOUBLE-CHECK] Re-validating all findings")
            await self._double_check_findings()
            await self._update_progress(80, "Double-check complete")

        # Finalization
        await self.log("info", "[FINAL] AI Finding Enhancement")
        await self._ai_enhance_findings()
        await self._update_progress(92, "Findings enhanced")

        await self.log("info", "[FINAL] Report Generation")
        report = await self._generate_full_report()
        await self._update_progress(100, "Auto pentest complete")

        if self.execution_history:
            self.execution_history.flush()

        if self.reasoning_memory and self.findings:
            try:
                vuln_types_found = list({f.vulnerability_type for f in self.findings})
                for tech in self.recon.technologies[:3]:
                    self.reasoning_memory.record_strategy(
                        technology=tech, vuln_types_found=vuln_types_found,
                        priority_order=[f.vulnerability_type for f in sorted(
                            self.findings, key=lambda f: getattr(f, 'confidence_score', 50), reverse=True
                        )][:10],
                        insights=[f"{f.vulnerability_type}: {f.affected_endpoint[:50]}"
                                  for f in self.findings[:5]]
                    )
                self.reasoning_memory.flush()
            except Exception:
                pass

        if self._checkpoint_manager:
            self._checkpoint_manager.delete()

        await self.log("info", f"  AUTO PENTEST COMPLETE: {len(self.findings)} findings")
        return report

    # ═══════════════════════ STREAM 1: Recon ═══════════════════════

    async def _stream_recon(self):
        """Stream 1: Active reconnaissance pipeline."""
        await self.log("info", "[STREAM 1] Recon starting")
        await self._update_progress(2, "Recon: starting")

        if self.recon_context:
            await self._feed_recon_context()
        else:
            await self._run_http_recon()

        # Push endpoints to queue for junior pentester
        for ep in self.recon.endpoints[:50]:
            await self._endpoint_queue.put(ep)

        self._recon_complete.set()
        await self.log("info", f"[STREAM 1] Recon complete: {len(self.recon.endpoints)} endpoints")

    async def _feed_recon_context(self):
        """Feed existing recon context into agent state."""
        ctx = self.recon_context or {}
        data = ctx.get("data", {}) or ctx

        if data.get("endpoints"):
            for ep in data["endpoints"][:100]:
                url = ep.get("url", "") if isinstance(ep, dict) else str(ep)
                if url and url not in [_get_endpoint_url(e) for e in self.recon.endpoints]:
                    self.recon.endpoints.append({"url": url, "method": "GET", "source": "context"})

        if data.get("urls"):
            for u in data["urls"][:100]:
                if u not in [_get_endpoint_url(e) for e in self.recon.endpoints]:
                    self.recon.endpoints.append({"url": u, "method": "GET", "source": "context"})

        if data.get("technologies"):
            self.recon.technologies = list(set(self.recon.technologies + data["technologies"]))

        if data.get("parameters"):
            if isinstance(data["parameters"], dict):
                self.recon.parameters.update(data["parameters"])
            elif isinstance(data["parameters"], list):
                for p in data["parameters"]:
                    self.recon.parameters.setdefault(self.target, []).append(str(p))

    async def _run_http_recon(self):
        """HTTP-only recon: no Docker tools, graceful degradation."""
        await self.log("info", "[RECON] Starting HTTP-based reconnaissance")

        techs = await self._fingerprint_target()
        if techs:
            self.recon.technologies = techs

        common_paths = [
            "/", "/robots.txt", "/sitemap.xml", "/.git/config", "/.env",
            "/api", "/api/v1", "/api/v2", "/graphql", "/swagger",
            "/admin", "/login", "/register", "/dashboard",
            "/wp-admin", "/wp-login.php", "/phpmyadmin",
            "/actuator", "/actuator/health",
        ]

        for path in common_paths:
            if self.is_cancelled():
                break
            try:
                url = f"{self.target.rstrip('/')}{path}"
                async with self.session.get(url, allow_redirects=False) as resp:
                    if resp.status < 404:
                        self.recon.endpoints.append({
                            "url": url, "path": path, "status": resp.status,
                            "method": "GET", "source": "recon_path_check",
                        })
                    if resp.status not in (404, 500):
                        parsed = urlparse(url)
                        if parsed.query:
                            params = list(parse_qs(parsed.query).keys())
                            self.recon.parameters.setdefault(url, []).extend(params)
            except Exception:
                pass

        await self.log("info", f"[RECON] Found {len(self.recon.endpoints)} endpoints")

    async def _fingerprint_target(self) -> List[str]:
        """Fingerprint target technology stack."""
        technologies = []
        try:
            async with self.session.get(self.target) as resp:
                body = await resp.text()
                headers = dict(resp.headers)

                server = headers.get("Server", "")
                if server:
                    technologies.append(f"Server: {server}")

                powered = headers.get("X-Powered-By", "")
                if powered:
                    technologies.append(powered)

                tech_sigs = {
                    "PHP": [".php", "PHPSESSID"], "ASP.NET": [".aspx", "__VIEWSTATE"],
                    "Java": [".jsp", "JSESSIONID"], "Python": ["django", "flask"],
                    "Node.js": ["express", "connect.sid"],
                    "WordPress": ["wp-content", "wp-includes"],
                    "Laravel": ["laravel", "XSRF-TOKEN"],
                }
                for tech, sigs in tech_sigs.items():
                    for sig in sigs:
                        if sig.lower() in body.lower() or sig in str(headers):
                            technologies.append(tech)
                            break
        except Exception:
            pass
        return list(set(technologies))

    # ═══════════════════════ STREAM 2: Junior Pentester ═══════════════════════

    async def _stream_junior_pentest(self):
        """Stream 2: Immediate AI-driven testing as endpoints are discovered."""
        await self.log("info", "[STREAM 2] Junior pentester ready")
        await self._update_progress(5, "Junior: waiting for endpoints")

        while not self._recon_complete.is_set() or not self._endpoint_queue.empty():
            if self.is_cancelled():
                break

            try:
                ep = await asyncio.wait_for(self._endpoint_queue.get(), timeout=2.0)
            except asyncio.TimeoutError:
                continue

            url = _get_endpoint_url(ep)
            if not url:
                continue

            # Quick test: check 10 high-priority vuln types
            quick_types = ["sqli_error", "xss_reflected", "command_injection", "ssti",
                          "lfi", "ssrf", "open_redirect", "idor", "path_traversal", "xxe"]

            for vt in quick_types:
                if self.is_cancelled():
                    return
                if vt in self._junior_tested_types:
                    continue

                payloads = self._get_payloads(vt)[:3]
                if not payloads:
                    continue

                params = self.recon.parameters.get(url, ["id", "q", "search"])
                for param in params[:2]:
                    for payload in payloads[:2]:
                        resp = await self._make_request_with_injection(url, "GET", payload, "parameter", param)
                        if not resp:
                            continue
                        is_vuln, evidence = await self._verify_vulnerability(vt, payload, resp, None)
                        if is_vuln:
                            finding = self._create_finding(vt, url, param, payload, evidence, resp, ai_confirmed=True)
                            await self._add_finding(finding)
                            self._stream_findings_count += 1
                            await self.log("warning", f"  [JUNIOR] {vt} at {url[:50]}")
                            break

                self._junior_tested_types.add(vt)

        await self.log("info", f"[STREAM 2] Junior complete: {self._stream_findings_count} findings")

    # ═══════════════════════ STREAM 3: Tool Runner ═══════════════════════

    async def _stream_tool_runner(self):
        """Stream 3: Dynamic tool execution (HTTP-based, graceful degradation).

        No Docker/Kali sandbox. Runs tools natively via subprocess.
        Gracefully skips unavailable tools.
        """
        await self.log("info", "[STREAM 3] Tool runner starting")
        available_tools = self._check_available_tools()
        await self.log("info", f"[STREAM 3] Tools: {', '.join(available_tools) or 'none available'}")

        if not available_tools:
            await self.log("info", "[STREAM 3] No tools available — using AI analysis only")
            # Run AI-driven analysis instead
            if self.llm.is_available():
                await self._ai_analyze_attack_surface()
            self._tools_complete.set()
            return

        tools_to_run = []
        target_domain = self.target.replace("https://", "").replace("http://", "").split("/")[0]

        for tool in available_tools:
            if self.is_cancelled():
                break
            if tool == "nuclei":
                tools_to_run.append(asyncio.create_task(
                    self._run_tool_nuclei(self.target, tool)
                ))
            elif tool == "nmap":
                tools_to_run.append(asyncio.create_task(
                    self._run_tool_cmd("nmap", ["nmap", "-sT", "-T4", "--top-ports", "100", "-oG", "-", target_domain])
                ))
            elif tool == "whatweb":
                tools_to_run.append(asyncio.create_task(
                    self._run_tool_cmd("whatweb", ["whatweb", "-q", "-a", "3", "--color=never", self.target])
                ))
            elif tool == "ffuf" and Path("/opt/wordlists/common.txt").exists():
                tools_to_run.append(asyncio.create_task(
                    self._run_tool_cmd("ffuf", ["ffuf", "-u", f"{self.target}/FUZZ", "-w", "/opt/wordlists/common.txt",
                                                "-mc", "200,201,204,301,302,307", "-t", "30", "-o", "-", "-of", "json"])
                ))

        if tools_to_run:
            results = await asyncio.gather(*tools_to_run, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    await self.log("debug", f"[STREAM 3] Tool error: {result}")

        self._tools_complete.set()
        await self.log("info", "[STREAM 3] Tool runner complete")

    def _check_available_tools(self) -> List[str]:
        """Check which security tools are available on PATH."""
        tools = ["nmap", "nuclei", "nikto", "sqlmap", "ffuf", "gobuster",
                 "whatweb", "wafw00f", "katana", "subfinder", "naabu", "dnsx"]
        available = []
        for tool in tools:
            try:
                result = subprocess.run(["which", tool], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    available.append(tool)
            except Exception:
                pass
        return available

    async def _run_tool_cmd(self, tool_name: str, cmd: List[str]) -> Optional[str]:
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=300)
            output = stdout.decode('utf-8', errors='replace')
            await self.log("debug", f"[TOOL] {tool_name} completed ({process.returncode})")
            return output
        except asyncio.TimeoutError:
            await self.log("debug", f"[TOOL] {tool_name} timed out")
            return None
        except Exception as e:
            await self.log("debug", f"[TOOL] {tool_name} error: {e}")
            return None

    async def _run_tool_nuclei(self, target: str, tool_name: str):
        output = await self._run_tool_cmd("nuclei", [
            "nuclei", "-u", target, "-severity", "critical,high,medium",
            "-silent", "-json", "-c", "25",
        ])
        if output:
            for line in output.strip().split("\n"):
                try:
                    vuln = json.loads(line)
                    info = vuln.get("info", {})
                    finding = Finding(
                        id=hashlib.md5(f"{info.get('name', '')}|{vuln.get('matched-at', target)}".encode()).hexdigest()[:12],
                        title=info.get("name", "Nuclei Finding"),
                        severity=info.get("severity", "medium"),
                        vulnerability_type=info.get("tags", ["vulnerability"])[0],
                        description=info.get("description", ""),
                        affected_endpoint=vuln.get("matched-at", target),
                        evidence=vuln.get("matcher-name", ""),
                        remediation=info.get("remediation", "Review and fix"),
                        references=info.get("reference", []),
                    )
                    if self.memory:
                        self.memory.add_confirmed_finding(finding)
                except Exception:
                    pass

    # ═══════════════════════ CLI Agent Mode (graceful degradation) ═══════════════════════

    async def _run_cli_agent_mode(self) -> Dict:
        """CLI Agent mode — no sandbox, returns gracefully degraded result."""
        await self.log("info", "=" * 60)
        await self.log("info", "  CLI AGENT MODE (graceful degradation)")
        await self.log("info", "  No Docker sandbox available — using agent analysis")
        await self.log("info", "=" * 60)
        await self._update_progress(0, "CLI Agent (degraded)")

        # Run recon and standard testing instead
        await self._run_http_recon()
        attack_plan = await self._ai_analyze_attack_surface()
        await self._test_all_vulnerabilities(attack_plan)
        await self._ai_enhance_findings()

        report = await self._generate_full_report()
        await self._update_progress(100, "CLI Agent complete (degraded)")
        return report

    # ═══════════════════════ FULL LLM PENTEST ═══════════════════════

    async def _run_full_llm_pentest(self) -> Dict:
        """Full LLM Pentest: AI drives every step of the pentest."""
        await self._update_progress(0, "Full LLM Pentest starting")
        await self.log("info", "=" * 60)
        await self.log("info", "  FULL LLM PENTEST MODE")
        await self.log("info", "=" * 60)

        if not self.llm.is_available():
            await self.log("error", "LLM not available for Full LLM Pentest")
            return self._generate_error_report("LLM not available")

        try:
            from app.core.neurosploit.ai_prompts import (
                get_full_llm_pentest_system_prompt,
                get_full_llm_pentest_round_prompt,
            )
        except ImportError:
            from app.core.neurosploit.pentest_playbook import (
                get_playbook_entry, build_agent_testing_prompt
            )

        methodology = self.custom_prompt or ""
        system_prompt = methodology or DEFAULT_ASSESSMENT_PROMPT

        discovered_info_parts = []
        all_round_results = []
        MAX_ROUNDS = 20

        for round_num in range(1, MAX_ROUNDS + 1):
            if self.is_cancelled():
                break

            progress = min(85, int((round_num / MAX_ROUNDS) * 85))
            await self._update_progress(progress, f"LLM Pentest Round {round_num}/{MAX_ROUNDS}")

            recent = "\n\n".join(all_round_results[-5:]) if all_round_results else ""
            discovered = "\n".join(discovered_info_parts[-30:]) if discovered_info_parts else ""

            round_prompt = f"""Round {round_num}/{MAX_ROUNDS} against {self.target}.

Previously discovered:
{discovered}

Recent actions:
{recent}

Plan your next actions. Output JSON:
{{"actions": [{{"method": "GET", "url": "/path", "params": {{}}, "purpose": ""}}], "findings": []}}"""

            try:
                response = await self.llm.generate(round_prompt, system_prompt)
                all_round_results.append(f"Round {round_num}: {response[:500]}")

                match = re.search(r'\{[\s\S]*\}', response)
                if match:
                    data = json.loads(match.group())
                    for action in data.get("actions", [])[:10]:
                        try:
                            method = action.get("method", "GET")
                            url = action.get("url", self.target)
                            params = action.get("params", {})
                            purpose = action.get("purpose", "")

                            full_url = url if url.startswith("http") else f"{self.target.rstrip('/')}{url}"
                            async with self.session.request(method, full_url, params=params) as resp:
                                body = await resp.text()
                                discovered_info_parts.append(
                                    f"{method} {full_url} → {resp.status} ({len(body)}B) [{purpose}]"
                                )
                        except Exception:
                            pass

                    for finding in data.get("findings", []):
                        f = Finding(
                            title=finding.get("title", "LLM Finding"),
                            severity=finding.get("severity", "medium"),
                            vulnerability_type=finding.get("type", "unknown"),
                            description=finding.get("description", ""),
                            affected_endpoint=finding.get("endpoint", self.target),
                            evidence=finding.get("evidence", ""),
                            ai_verified=True, ai_status="confirmed",
                        )
                        await self._add_finding(f)
            except Exception as e:
                await self.log("debug", f"LLM round error: {e}")

        await self._ai_enhance_findings()
        report = await self._generate_full_report()
        await self._update_progress(100, "Full LLM Pentest complete")
        return report

    # ═══════════════════════ Core Testing Methods ═══════════════════════

    async def _make_request_with_injection(self, url: str, method: str, payload: str,
                                            injection_point: str = "parameter",
                                            param_name: str = "test",
                                            header_name: str = "") -> Optional[Dict]:
        try:
            if injection_point == "header" and header_name:
                headers = {**dict(self.session._default_headers),
                           header_name: payload}
                async with self.session.request(method, url, headers=headers) as resp:
                    body = await resp.text()
                    return {"status": resp.status, "body": body,
                            "headers": dict(resp.headers), "url": str(resp.url)}
            elif injection_point == "parameter":
                params = {param_name: payload}
                async with self.session.request(method, url, params=params) as resp:
                    body = await resp.text()
                    return {"status": resp.status, "body": body,
                            "headers": dict(resp.headers), "url": str(resp.url)}
            elif injection_point == "body":
                async with self.session.request(method, url, data={param_name: payload}) as resp:
                    body = await resp.text()
                    return {"status": resp.status, "body": body,
                            "headers": dict(resp.headers), "url": str(resp.url)}
            else:
                async with self.session.request(method, url, params={param_name: payload}) as resp:
                    body = await resp.text()
                    return {"status": resp.status, "body": body,
                            "headers": dict(resp.headers), "url": str(resp.url)}
        except Exception:
            return None

    async def _verify_vulnerability(self, vuln_type: str, payload: str,
                                      resp: Optional[Dict], baseline: Optional[Dict]) -> Tuple[bool, str]:
        if not resp:
            return False, "No response"

        body = resp.get("body", "")
        status = resp.get("status", 0)

        if vuln_type in ("sqli_error", "sqli_union", "sqli_blind", "sqli_time"):
            sql_errors = ["sql syntax", "mysql_", "sqlite_", "pg_query", "ora-",
                          "warning: mysql", "unclosed quotation"]
            for err in sql_errors:
                if err in body.lower():
                    return True, f"SQL error: {err}"
            return False, "No SQL error indicators"

        if vuln_type in ("xss_reflected", "xss_stored", "xss_dom"):
            if payload in body and "<" in payload:
                return True, "XSS payload reflected without encoding"
            return False, "Payload not reflected"

        if vuln_type == "command_injection":
            rce_indicators = ["uid=", "gid=", "groups=", "/bin/", "/usr/"]
            for ind in rce_indicators:
                if ind in body.lower():
                    return True, f"Command output: {ind}"
            return False, "No RCE indicators"

        if vuln_type == "ssti":
            if "49" in body and "7*7" in payload:
                return True, "SSTI: 7*7=49 evaluated"
            return False, "No SSTI evaluation"

        if vuln_type == "lfi":
            if "root:" in body:
                return True, "LFI: /etc/passwd content found"
            return False, "No file content found"

        if vuln_type == "ssrf":
            for ind in ["root:", "localhost", "meta-data", "169.254"]:
                if ind in body.lower():
                    return True, f"SSRF: {ind}"
            return False, "No SSRF indicators"

        if self.validation_judge:
            try:
                result = await self.validation_judge.judge(vuln_type, payload, resp, baseline)
                if result.get("confirmed"):
                    return True, result.get("explanation", "Confirmed by validation judge")
            except Exception:
                pass

        return False, "No vulnerability indicators"

    def _create_finding(self, vuln_type: str, url: str, param: str, payload: str,
                         evidence: str, resp: Optional[Dict], ai_confirmed: bool = False) -> Finding:
        mapped = self._map_vuln_type(vuln_type)
        finding = Finding(
            id=hashlib.md5(f"{vuln_type}|{url}|{param}|{payload}".encode()).hexdigest()[:12],
            title=self.vuln_registry.get_title(mapped) if self.vuln_registry else f"{vuln_type} at {url[:50]}",
            severity=self.vuln_registry.get_severity(mapped) if self.vuln_registry else "medium",
            vulnerability_type=vuln_type,
            cvss_score=self._get_cvss_score(vuln_type),
            cvss_vector=self._get_cvss_vector(vuln_type),
            cwe_id=self.vuln_registry.get_cwe_id(mapped) if self.vuln_registry else "",
            description=self.vuln_registry.get_description(mapped) if self.vuln_registry else evidence,
            affected_endpoint=url,
            parameter=param,
            payload=payload,
            evidence=evidence,
            request=resp.get("url", url) if resp else "",
            response=resp.get("body", "")[:2000] if resp else "",
            impact=f"Vulnerability in {param} parameter",
            remediation="Review and fix the vulnerable parameter",
            ai_verified=ai_confirmed,
            confidence_score=75 if ai_confirmed else 50,
            confidence="high" if ai_confirmed else "medium",
            ai_status="confirmed" if ai_confirmed else "pending",
        )
        return finding

    async def _add_finding(self, finding: Finding):
        """Add a finding through the validation pipeline."""
        if self.memory:
            if self.memory.has_finding_for(finding.vulnerability_type, finding.affected_endpoint):
                return

        if self.validation_judge:
            try:
                verdict = await self.validation_judge.judge(
                    finding.vulnerability_type, finding.payload,
                    {"status": 200, "body": finding.evidence}, None
                )
                if verdict.get("confirmed"):
                    finding.confidence_score = verdict.get("confidence", 75)
                    finding.confidence = "high" if finding.confidence_score >= 80 else "medium"
                    finding.ai_verified = True
                    finding.ai_status = "confirmed"
                elif verdict.get("rejected"):
                    finding.ai_status = "rejected"
                    finding.rejection_reason = verdict.get("reason", "")
                    self.rejected_findings.append(finding)
                    return
            except Exception:
                pass

        if self.memory:
            self.memory.add_confirmed_finding(finding)

        if self.finding_callback:
            try:
                await self.finding_callback(finding)
            except Exception:
                pass

    # ═══════════════════════ Analysis & Planning ═══════════════════════

    async def _ai_master_plan(self) -> Dict:
        """AI strategic master plan before launching parallel streams."""
        if not self.llm.is_available():
            return {}

        technologies_str = ", ".join(self.recon.technologies[:10]) or "Unknown"

        prompt = f"""You are planning a penetration test against {self.target}.

Technology Stack: {technologies_str}

Provide a strategic master plan with:
1. Target profile (what kind of app is this?)
2. Risk assessment (what are the biggest risks?)
3. Priority vulnerability types (top 5-10 to test first)
4. Recommended tools (from: nmap, nuclei, sqlmap, ffuf, whatweb)

Output JSON:
{{"target_profile": "...", "risk_assessment": "...", "priority_vuln_types": ["sqli_error", ...], "recommended_tools": ["nuclei", ...]}}"""

        try:
            response = await self.llm.generate(prompt, "You are a senior penetration tester.")
            match = re.search(r'\{[\s\S]*\}', response)
            if match:
                return json.loads(match.group())
        except Exception:
            pass
        return {}

    def _default_attack_plan(self) -> Dict:
        return {
            "priority_vulns": [
                "sqli_error", "xss_reflected", "command_injection", "ssti",
                "lfi", "ssrf", "idor", "path_traversal", "xxe", "security_headers",
                "csrf", "open_redirect", "cors_misconfig", "clickjacking",
                "nosql_injection", "file_upload", "jwt_manipulation",
                "host_header_injection", "crlf_injection", "rate_limit_bypass",
            ]
        }

    async def _ai_analyze_attack_surface(self) -> Dict:
        """AI analysis of attack surface to prioritize testing."""
        if not self.llm.is_available():
            return self._default_attack_plan()

        endpoints_str = "\n".join([
            f"- {_get_endpoint_method(ep)} {_get_endpoint_url(ep)}"
            for ep in self.recon.endpoints[:20]
        ]) or "None discovered"

        params_str = "\n".join([
            f"- {url}: {', '.join(p[:3] if isinstance(p, list) else [str(p)])}"
            for url, p in list(self.recon.parameters.items())[:10]
        ]) if isinstance(self.recon.parameters, dict) else "None"

        technologies_str = ", ".join(self.recon.technologies) or "Unknown"

        prompt = f"""Analyze this attack surface:

Target: {self.target}
Technologies: {technologies_str}
Endpoints ({len(self.recon.endpoints)} total):
{endpoints_str}

Parameters:
{params_str}

Based on this, prioritize vulnerability tests. Return JSON:
{{"priority_vulns": ["sqli_error", "xss_reflected", ...],
  "notes": "specific observations about the target"}}"""

        try:
            response = await self.llm.generate(prompt, "You are a security researcher.")
            match = re.search(r'\{[\s\S]*\}', response)
            if match:
                plan = json.loads(match.group())
                if plan.get("priority_vulns"):
                    return plan
        except Exception:
            pass
        return self._default_attack_plan()

    async def _test_all_vulnerabilities(self, attack_plan: Dict):
        """Execute the comprehensive vulnerability testing phase."""
        vuln_types = attack_plan.get("priority_vulns", [])[:30]

        for vt in vuln_types:
            if self.is_cancelled():
                return

            payloads = self._get_payloads(vt)[:5]
            if not payloads:
                continue

            for ep in self.recon.endpoints[:15]:
                if self.is_cancelled():
                    return

                url = _get_endpoint_url(ep)
                if not url:
                    continue

                params = self.recon.parameters.get(url, [])
                if not params:
                    parsed = urlparse(url)
                    if parsed.query:
                        params = list(parse_qs(parsed.query).keys())
                    else:
                        params = ["id", "q", "search"]

                for param in params[:3]:
                    for payload in payloads[:3]:
                        resp = await self._make_request_with_injection(
                            url, "GET", payload, "parameter", param
                        )
                        if not resp:
                            continue

                        is_vuln, evidence = await self._verify_vulnerability(vt, payload, resp, None)
                        if is_vuln:
                            finding = self._create_finding(
                                vt, url, param, payload, evidence, resp,
                                ai_confirmed=True
                            )
                            await self._add_finding(finding)
                            await self.log("warning", f"  [{vt}] CONFIRMED at {url[:50]}")
                            break

    async def _double_check_findings(self):
        """Re-validate all findings to eliminate false positives."""
        if not self.validation_judge:
            return
        for finding in self.findings:
            if finding.double_checked:
                continue
            try:
                verdict = await self.validation_judge.retest(finding)
                if verdict.get("rejected"):
                    finding.ai_status = "rejected"
                    finding.rejection_reason = verdict.get("reason", "")
                else:
                    finding.double_checked = True
            except Exception:
                pass

    async def _ai_enhance_findings(self):
        """Use AI to enhance finding descriptions, impact, and remediation."""
        if not self.llm.is_available():
            return

        for finding in self.findings[:20]:
            if self.is_cancelled():
                break
            try:
                prompt = f"""Enhance this vulnerability finding:

Type: {finding.vulnerability_type}
Endpoint: {finding.affected_endpoint}
Parameter: {finding.parameter}
Evidence: {finding.evidence[:300]}

Return JSON:
{{"description": "...", "impact": "...", "remediation": "..."}}"""

                response = await self.llm.generate(prompt, "Enhance security findings professionally.")
                match = re.search(r'\{[\s\S]*\}', response)
                if match:
                    enhanced = json.loads(match.group())
                    if enhanced.get("description"):
                        finding.description = enhanced["description"]
                    if enhanced.get("impact"):
                        finding.impact = enhanced["impact"]
                    if enhanced.get("remediation"):
                        finding.remediation = enhanced["remediation"]
            except Exception:
                pass

    # ═══════════════════════ CVSS Scoring ═══════════════════════

    def _get_cvss_score(self, vuln_type: str) -> float:
        scores = {"sqli_error": 7.5, "sqli_union": 8.5, "sqli_blind": 7.5, "sqli_time": 7.5,
                  "command_injection": 9.8, "ssti": 9.8, "xss_reflected": 6.1, "xss_stored": 8.5,
                  "lfi": 7.5, "rfi": 9.8, "path_traversal": 7.5, "ssrf": 7.5, "ssrf_cloud": 9.8,
                  "xxe": 8.6, "csrf": 6.5, "idor": 6.5, "clickjacking": 3.1, "open_redirect": 4.7,
                  "file_upload": 8.8, "security_headers": 0.0, "cors_misconfig": 5.4}
        return scores.get(self._map_vuln_type(vuln_type), 5.0)

    def _get_cvss_vector(self, vuln_type: str) -> str:
        vectors = {"sqli_error": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                   "command_injection": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                   "ssti": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                   "xss_reflected": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N",
                   "lfi": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                   "ssrf": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"}
        return vectors.get(self._map_vuln_type(vuln_type),
                           "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N")

    # ═══════════════════════ Report Generation ═══════════════════════

    async def _generate_full_report(self) -> Dict:
        """Generate comprehensive pentest report."""
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        for f in self.findings:
            severity_counts[f.severity] = severity_counts.get(f.severity, 0) + 1

        report = {
            "target": self.target,
            "scan_date": datetime.utcnow().isoformat(),
            "agent": "NeuroSploit AI Agent v3",
            "mode": self.mode.value,
            "summary": {
                "total_findings": len(self.findings),
                "critical": severity_counts["critical"],
                "high": severity_counts["high"],
                "medium": severity_counts["medium"],
                "low": severity_counts["low"],
                "info": severity_counts["info"],
                "endpoints_analyzed": len(self.recon.endpoints),
                "technologies_detected": self.recon.technologies,
            },
            "findings": [],
            "recommendations": [],
            "rejected_findings": [],
        }

        for finding in self.findings:
            report["findings"].append({
                "id": finding.id,
                "title": finding.title,
                "severity": finding.severity,
                "vulnerability_type": finding.vulnerability_type,
                "cvss_score": finding.cvss_score,
                "cvss_vector": finding.cvss_vector,
                "cwe_id": finding.cwe_id,
                "description": finding.description,
                "affected_endpoint": finding.affected_endpoint,
                "parameter": finding.parameter,
                "payload": finding.payload,
                "evidence": finding.evidence,
                "impact": finding.impact,
                "poc_code": finding.poc_code,
                "remediation": finding.remediation,
                "ai_verified": finding.ai_verified,
                "confidence_score": finding.confidence_score,
                "confidence": finding.confidence,
            })

        # Sort findings by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        report["findings"].sort(key=lambda x: severity_order.get(x["severity"], 5))

        # Recommendations
        remediations = []
        for f in self.findings:
            if f.remediation and f.remediation not in remediations:
                remediations.append(f.remediation)
        report["recommendations"] = [
            r for r in remediations[:20]
        ] or ["Address identified vulnerabilities", "Implement security headers",
              "Keep software updated", "Enable proper logging"]

        return report

    def _generate_error_report(self, error_msg: str) -> Dict:
        return {
            "target": self.target,
            "error": error_msg,
            "findings": [f.__dict__ if hasattr(f, '__dict__') else f
                         for f in self.findings],
            "summary": {"total_findings": len(self.findings)},
        }

    # ═══════════════════════ Status & Diagnostics ═══════════════════════

    def get_llm_status(self) -> Dict:
        return self.llm.get_status()

    def get_agent_status(self) -> Dict:
        return {
            "target": self.target,
            "mode": self.mode.value,
            "cancelled": self._cancelled,
            "paused": self._paused,
            "progress": self._last_progress,
            "phase": self._last_phase,
            "endpoints": len(self.recon.endpoints),
            "technologies": self.recon.technologies,
            "findings": len(self.findings),
            "rejected": len(self.rejected_findings),
            "junior_tested_types": len(self._junior_tested_types),
        }