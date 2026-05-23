import json
import logging
import os
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin

import aiohttp

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 1.0
RETRY_MULTIPLIER = 2.0


@dataclass
class LLMResponse:
    content: str
    provider: str
    model: str
    tokens_used: int = 0
    latency_ms: float = 0.0
    is_error: bool = False
    error_message: str = ""


class LLMManager:

    PROVIDERS = {"openai", "claude", "gemini", "openrouter", "ollama", "lmstudio"}

    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4o",
        api_key: str = "",
        temperature: float = 0.0,
        max_tokens: int = 4096,
        base_url: str = "",
        timeout: float = 120.0,
        guardrails: bool = False,
        hallucination_strategy: Optional[str] = None,
    ):
        self.provider = provider.lower()
        self.model = model
        self.api_key = api_key or self._env_api_key()
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.base_url = base_url or self._env_base_url()
        self.timeout = timeout
        self.guardrails = guardrails
        self.hallucination_strategy = hallucination_strategy
        self._prompts: Dict[str, Dict[str, str]] = {}

    @classmethod
    def from_env(cls) -> "LLMManager":
        provider = os.getenv("NEUROSPLOIT_LLM_PROVIDER", "openai").lower()
        model = os.getenv("NEUROSPLOIT_LLM_MODEL", "gpt-4o")
        api_key = ""
        base_url = ""
        if provider == "claude":
            api_key = os.getenv("ANTHROPIC_API_KEY", "")
            base_url = os.getenv("ANTHROPIC_BASE_URL", "")
            model = model or "claude-sonnet-4-20250514"
        elif provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY", "")
            base_url = os.getenv("OPENAI_BASE_URL", "")
            model = model or "gpt-4o"
        elif provider == "gemini":
            api_key = os.getenv("GOOGLE_API_KEY", "")
            base_url = os.getenv("GEMINI_BASE_URL", "")
            model = model or "gemini-2.0-flash"
        elif provider == "openrouter":
            api_key = os.getenv("OPENROUTER_API_KEY", "")
            model = model or "anthropic/claude-sonnet-4-20250514"
        temperature = float(os.getenv("NEUROSPLOIT_LLM_TEMPERATURE", "0.0"))
        max_tokens = int(os.getenv("NEUROSPLOIT_LLM_MAX_TOKENS", "4096"))
        max_out = os.getenv("MAX_OUTPUT_TOKENS", "").strip()
        if max_out:
            try:
                max_tokens = int(max_out)
            except ValueError:
                pass
        guardrails = os.getenv("NEUROSPLOIT_GUARDRAILS", "false").lower() == "true"
        strategy = os.getenv("NEUROSPLOIT_HALLUCINATION_STRATEGY", None)
        return cls(
            provider=provider, model=model, api_key=api_key,
            temperature=temperature, max_tokens=max_tokens,
            base_url=base_url, guardrails=guardrails,
            hallucination_strategy=strategy,
        )

    def _env_api_key(self) -> str:
        mapping = {
            "claude": "ANTHROPIC_API_KEY",
            "openai": "OPENAI_API_KEY",
            "gemini": "GOOGLE_API_KEY",
            "openrouter": "OPENROUTER_API_KEY",
        }
        env_var = mapping.get(self.provider, "NEUROSPLOIT_LLM_API_KEY")
        return os.getenv(env_var, "")

    def _env_base_url(self) -> str:
        mapping = {
            "claude": "ANTHROPIC_BASE_URL",
            "openai": "OPENAI_BASE_URL",
            "gemini": "GEMINI_BASE_URL",
        }
        env_var = mapping.get(self.provider, "")
        return os.getenv(env_var, "")

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> LLMResponse:
        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens if max_tokens is not None else self.max_tokens
        start = time.monotonic()
        raw = ""
        try:
            if self.provider == "claude":
                raw = await self._claude(prompt, system_prompt, temp, tokens)
            elif self.provider == "openai":
                raw = await self._openai(prompt, system_prompt, temp, tokens)
            elif self.provider == "gemini":
                raw = await self._gemini(prompt, system_prompt, temp, tokens)
            elif self.provider == "openrouter":
                raw = await self._openrouter(prompt, system_prompt, temp, tokens)
            elif self.provider == "ollama":
                raw = await self._ollama(prompt, system_prompt, temp, tokens)
            elif self.provider == "lmstudio":
                raw = await self._lmstudio(prompt, system_prompt, temp, tokens)
            else:
                return LLMResponse(
                    content="", provider=self.provider, model=self.model,
                    is_error=True, error_message=f"Unsupported provider: {self.provider}",
                    latency_ms=(time.monotonic() - start) * 1000,
                )
        except Exception as e:
            logger.error(f"LLM generate error ({self.provider}): {e}")
            return LLMResponse(
                content="", provider=self.provider, model=self.model,
                is_error=True, error_message=str(e),
                latency_ms=(time.monotonic() - start) * 1000,
            )
        if self.guardrails:
            raw = self._apply_guardrails(raw)
        if self.hallucination_strategy in ("grounding", "self_reflection", "consistency_check"):
            raw = await self._mitigate_hallucination(raw, prompt, system_prompt or "")
        latency = (time.monotonic() - start) * 1000
        return LLMResponse(
            content=raw, provider=self.provider, model=self.model,
            latency_ms=latency,
        )

    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> tuple[bool, Any]:
        system = (system_prompt or "") + "\nRespond with valid JSON only."
        resp = await self.generate(prompt, system, **kwargs)
        if resp.is_error:
            return False, resp.error_message
        try:
            return True, json.loads(resp.content)
        except json.JSONDecodeError:
            try:
                cleaned = resp.content.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
                return True, json.loads(cleaned)
            except json.JSONDecodeError:
                return False, resp.content

    async def routed_generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        task_type: str = "default",
        routes: Optional[Dict[str, Dict]] = None,
        **kwargs,
    ) -> LLMResponse:
        if routes and task_type in routes:
            route = routes[task_type]
            mgr = LLMManager(
                provider=route.get("provider", self.provider),
                model=route.get("model", self.model),
                api_key=route.get("api_key", self.api_key),
                temperature=route.get("temperature", self.temperature),
                max_tokens=route.get("max_tokens", self.max_tokens),
                base_url=route.get("base_url", self.base_url),
            )
            return await mgr.generate(prompt, system_prompt, **kwargs)
        return await self.generate(prompt, system_prompt, **kwargs)

    async def _request_with_retry(self, url: str, headers: Dict, data: Dict) -> str:
        last_error = None
        for attempt in range(MAX_RETRIES):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url, headers=headers, json=data,
                        timeout=aiohttp.ClientTimeout(total=self.timeout),
                    ) as resp:
                        if resp.status == 200:
                            result = await resp.json()
                            return self._extract_text(result)
                        elif resp.status == 401:
                            raise ValueError(f"API auth failed: {resp.status}")
                        elif resp.status == 429:
                            last_error = f"Rate limit: {resp.status}"
                            if attempt < MAX_RETRIES - 1:
                                sleep = RETRY_DELAY * (RETRY_MULTIPLIER ** (attempt + 1))
                                await asyncio.sleep(sleep)
                                continue
                        elif resp.status >= 500:
                            last_error = f"Server error {resp.status}"
                            if attempt < MAX_RETRIES - 1:
                                sleep = RETRY_DELAY * (RETRY_MULTIPLIER ** attempt)
                                await asyncio.sleep(sleep)
                                continue
                        text = await resp.text()
                        raise ValueError(f"API error {resp.status}: {text}")
            except (aiohttp.ClientConnectionError, aiohttp.ClientOSError) as e:
                last_error = str(e)
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_DELAY * (RETRY_MULTIPLIER ** attempt))
                    continue
                raise ConnectionError(f"Connection failed after retries: {last_error}")
            except asyncio.TimeoutError:
                last_error = "Timeout"
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_DELAY * (RETRY_MULTIPLIER ** attempt))
                    continue
                raise ConnectionError(f"Timeout after retries")
        raise ConnectionError(f"Request failed after {MAX_RETRIES} retries: {last_error}")

    def _extract_text(self, result: Dict) -> str:
        if "choices" in result:
            return result["choices"][0].get("message", {}).get("content", "")
        elif "content" in result:
            if isinstance(result["content"], list):
                return result["content"][0].get("text", "")
            return result["content"]
        elif "candidates" in result:
            parts = result["candidates"][0].get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", "")
            return ""
        elif "output" in result:
            return result["output"]
        elif "response" in result:
            return result["response"]
        return json.dumps(result)

    async def _claude(self, prompt: str, system_prompt: Optional[str], temp: float, tokens: int) -> str:
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        url = self.base_url or "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        data: Dict[str, Any] = {
            "model": self.model,
            "max_tokens": tokens,
            "temperature": temp,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            data["system"] = system_prompt
        return await self._request_with_retry(url, headers, data)

    async def _openai(self, prompt: str, system_prompt: Optional[str], temp: float, tokens: int) -> str:
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set")
        url = (self.base_url or "https://api.openai.com/v1") + "/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        messages: List[Dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temp,
            "max_tokens": tokens,
        }
        return await self._request_with_retry(url, headers, data)

    async def _gemini(self, prompt: str, system_prompt: Optional[str], temp: float, tokens: int) -> str:
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not set")
        full = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        url = (self.base_url or "https://generativelanguage.googleapis.com/v1beta") + f"/models/{self.model}:generateContent?key={self.api_key}"
        data = {
            "contents": [{"parts": [{"text": full}]}],
            "generationConfig": {
                "temperature": temp,
                "maxOutputTokens": tokens,
            },
        }
        headers = {"Content-Type": "application/json"}
        return await self._request_with_retry(url, headers, data)

    async def _openrouter(self, prompt: str, system_prompt: Optional[str], temp: float, tokens: int) -> str:
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not set")
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/neurosploit",
            "X-Title": "NeuroSploit",
        }
        messages: List[Dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temp,
            "max_tokens": tokens,
        }
        return await self._request_with_retry(url, headers, data)

    async def _ollama(self, prompt: str, system_prompt: Optional[str], temp: float, tokens: int) -> str:
        url = "http://localhost:11434/api/generate"
        data: Dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temp,
                "num_predict": tokens,
            },
        }
        if system_prompt:
            data["system"] = system_prompt
        headers = {"Content-Type": "application/json"}
        return await self._request_with_retry(url, headers, data)

    async def _lmstudio(self, prompt: str, system_prompt: Optional[str], temp: float, tokens: int) -> str:
        url = "http://localhost:1234/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        messages: List[Dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temp,
            "max_tokens": tokens,
            "stream": False,
        }
        return await self._request_with_retry(url, headers, data)

    def _apply_guardrails(self, response: str) -> str:
        keywords = ["malicious_exploit_command", "destroy_system", "wipe_data"]
        for kw in keywords:
            if kw in response.lower():
                response = response.replace(kw, "[REDACTED]").replace(kw.upper(), "[REDACTED]")
        if any(bp in response.lower() for bp in ["perform illegal activity", "bypass security illegally"]):
            response = "[UNETHICAL CONTENT FLAGGED]\n" + response
        return response

    async def _mitigate_hallucination(self, raw: str, prompt: str, system: str) -> str:
        original = self.hallucination_strategy
        self.hallucination_strategy = None
        try:
            if original == "grounding":
                verification = f"Review the following response:\n---\n{raw}\n---\nBased ONLY on the context provided, is this factual? If not, correct it. If completely unsourced, state 'UNSOURCED'."
                resp = await self.generate(verification, "You are a fact-checker.")
                return resp.content if not resp.is_error else raw
            elif original == "self_reflection":
                reflection = f"Critically review:\nOriginal: {prompt}\nResponse: {raw}\nIdentify hallucinations or inconsistencies. Provide corrected version if issues found, else state 'ACCURATE'."
                resp = await self.generate(reflection, "You evaluate AI-generated content.")
                return resp.content if not resp.is_error else raw
            elif original == "consistency_check":
                responses = []
                for _ in range(3):
                    r = await self.generate(prompt, system)
                    responses.append(r.content if not r.is_error else raw)
                if len(set(responses)) == 1:
                    return responses[0]
                synthesis = f"Synthesize a single consistent response from:\n" + "\n---\n".join(responses)
                resp = await self.generate(synthesis, "Synthesize consistent information from multiple sources.")
                return resp.content if not resp.is_error else raw
            return raw
        finally:
            self.hallucination_strategy = original