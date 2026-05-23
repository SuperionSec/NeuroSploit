import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class NeuroSploitConfig:
    llm_provider: str = "openai"
    llm_model: str = "gpt-4"
    llm_api_key: str = ""
    llm_temperature: float = 0.0
    llm_max_tokens: int = 4096
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    gemini_api_key: str = ""
    openrouter_api_key: str = ""
    openai_base_url: str = ""
    anthropic_base_url: str = ""
    gemini_base_url: str = ""
    max_retries: int = 3
    circuit_threshold: int = 5
    circuit_timeout: float = 30.0
    default_request_delay: float = 0.1
    default_timeout: float = 10.0
    max_concurrent_vuln_agents: int = 10
    enable_vuln_agents: bool = True
    scan_timeout: int = 3600
    confidence_threshold_confirmed: int = 90
    confidence_threshold_likely: int = 60
    extra_env: dict = field(default_factory=dict)

    @classmethod
    def from_env(cls, prefix: str = "NEUROSPLOIT_") -> "NeuroSploitConfig":
        cfg = cls()
        cfg.llm_provider = os.getenv(f"{prefix}LLM_PROVIDER", "openai").lower()
        cfg.llm_model = os.getenv(f"{prefix}LLM_MODEL", "gpt-4o")
        cfg.llm_api_key = os.getenv(f"{prefix}LLM_API_KEY", "")
        cfg.llm_temperature = float(os.getenv(f"{prefix}LLM_TEMPERATURE", "0.0"))
        cfg.llm_max_tokens = int(os.getenv(f"{prefix}LLM_MAX_TOKENS", "4096"))
        cfg.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        cfg.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        cfg.gemini_api_key = os.getenv("GOOGLE_API_KEY", "")
        cfg.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
        cfg.openai_base_url = os.getenv("OPENAI_BASE_URL", "")
        cfg.anthropic_base_url = os.getenv("ANTHROPIC_BASE_URL", "")
        cfg.gemini_base_url = os.getenv("GEMINI_BASE_URL", "")
        cfg.max_retries = int(os.getenv(f"{prefix}MAX_RETRIES", "3"))
        cfg.circuit_threshold = int(os.getenv(f"{prefix}CIRCUIT_THRESHOLD", "5"))
        cfg.circuit_timeout = float(os.getenv(f"{prefix}CIRCUIT_TIMEOUT", "30.0"))
        cfg.default_request_delay = float(os.getenv(f"{prefix}DEFAULT_REQUEST_DELAY", "0.1"))
        cfg.default_timeout = float(os.getenv(f"{prefix}DEFAULT_TIMEOUT", "10.0"))
        cfg.max_concurrent_vuln_agents = int(os.getenv(f"{prefix}MAX_CONCURRENT_VULN_AGENTS", "10"))
        cfg.enable_vuln_agents = os.getenv(f"{prefix}ENABLE_VULN_AGENTS", "true").lower() == "true"
        cfg.scan_timeout = int(os.getenv(f"{prefix}SCAN_TIMEOUT", "3600"))
        cfg.confidence_threshold_confirmed = int(os.getenv(f"{prefix}CONFIDENCE_THRESHOLD_CONFIRMED", "90"))
        cfg.confidence_threshold_likely = int(os.getenv(f"{prefix}CONFIDENCE_THRESHOLD_LIKELY", "60"))
        for key, val in os.environ.items():
            if key.startswith(prefix) and key not in (
                f"{prefix}LLM_PROVIDER", f"{prefix}LLM_MODEL", f"{prefix}LLM_API_KEY",
                f"{prefix}LLM_TEMPERATURE", f"{prefix}LLM_MAX_TOKENS",
                f"{prefix}MAX_RETRIES", f"{prefix}CIRCUIT_THRESHOLD",
                f"{prefix}CIRCUIT_TIMEOUT", f"{prefix}DEFAULT_REQUEST_DELAY",
                f"{prefix}DEFAULT_TIMEOUT", f"{prefix}MAX_CONCURRENT_VULN_AGENTS",
                f"{prefix}ENABLE_VULN_AGENTS", f"{prefix}SCAN_TIMEOUT",
                f"{prefix}CONFIDENCE_THRESHOLD_CONFIRMED", f"{prefix}CONFIDENCE_THRESHOLD_LIKELY",
            ):
                cfg.extra_env[key[len(prefix):].lower()] = val
        max_tokens_env = os.getenv("MAX_OUTPUT_TOKENS", "").strip()
        if max_tokens_env:
            try:
                override = int(max_tokens_env)
                cfg.llm_max_tokens = override
            except ValueError:
                pass
        return cfg

    def get_api_key_for_provider(self) -> str:
        if self.llm_provider == "claude":
            return self.anthropic_api_key or self.llm_api_key
        elif self.llm_provider == "openai":
            return self.openai_api_key or self.llm_api_key
        elif self.llm_provider == "gemini":
            return self.gemini_api_key or self.llm_api_key
        elif self.llm_provider == "openrouter":
            return self.openrouter_api_key or self.llm_api_key
        return self.llm_api_key

    def get_base_url_for_provider(self) -> str:
        if self.llm_provider == "claude":
            return self.anthropic_base_url
        elif self.llm_provider == "openai":
            return self.openai_base_url
        elif self.llm_provider == "gemini":
            return self.gemini_base_url
        return ""
