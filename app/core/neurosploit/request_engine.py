import asyncio
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, Optional, Any
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    SUCCESS = "success"
    CLIENT_ERROR = "client_error"
    RATE_LIMITED = "rate_limited"
    WAF_BLOCKED = "waf_blocked"
    SERVER_ERROR = "server_error"
    TIMEOUT = "timeout"
    CONNECTION_ERROR = "connection_error"


@dataclass
class RequestResult:
    status: int
    body: str
    headers: Dict[str, str]
    url: str
    error_type: ErrorType = ErrorType.SUCCESS
    retry_count: int = 0
    response_time: float = 0.0


@dataclass
class HostState:
    host: str
    request_count: int = 0
    error_count: int = 0
    consecutive_failures: int = 0
    last_request_time: float = 0.0
    delay: float = 0.1
    circuit_open: bool = False
    circuit_open_time: float = 0.0
    avg_response_time: float = 0.0
    _response_times: list = field(default_factory=list)


class RequestEngine:

    WAF_INDICATORS = [
        "cloudflare", "incapsula", "sucuri", "akamai", "imperva",
        "mod_security", "modsecurity", "request blocked", "access denied",
        "waf", "web application firewall", "barracuda", "fortinet",
        "f5 big-ip", "citrix", "azure firewall",
    ]

    def __init__(
        self,
        session,
        default_delay: float = 0.1,
        max_retries: int = 3,
        circuit_threshold: int = 5,
        circuit_timeout: float = 30.0,
        default_timeout: float = 10.0,
        is_cancelled_fn: Optional[Callable] = None,
    ):
        self.session = session
        self.default_delay = default_delay
        self.max_retries = max_retries
        self.circuit_threshold = circuit_threshold
        self.circuit_timeout = circuit_timeout
        self.default_timeout = default_timeout
        self.is_cancelled = is_cancelled_fn or (lambda: False)
        self._hosts: Dict[str, HostState] = {}
        self.total_requests = 0
        self.total_errors = 0
        self.errors_by_type: Dict[str, int] = {e.value: 0 for e in ErrorType}

    def _get_host(self, url: str) -> HostState:
        host = urlparse(url).netloc
        if host not in self._hosts:
            self._hosts[host] = HostState(host=host, delay=self.default_delay)
        return self._hosts[host]

    def _classify_error(self, status: int, body: str, exception: Optional[Exception] = None) -> ErrorType:
        if exception:
            exc_name = type(exception).__name__.lower()
            if "timeout" in exc_name or "timedout" in exc_name:
                return ErrorType.TIMEOUT
            return ErrorType.CONNECTION_ERROR
        if 200 <= status < 400:
            return ErrorType.SUCCESS
        if status == 429:
            return ErrorType.RATE_LIMITED
        if status == 403:
            body_lower = body.lower() if body else ""
            if any(w in body_lower for w in self.WAF_INDICATORS):
                return ErrorType.WAF_BLOCKED
            return ErrorType.CLIENT_ERROR
        if 400 <= status < 500:
            return ErrorType.CLIENT_ERROR
        if status >= 500:
            return ErrorType.SERVER_ERROR
        return ErrorType.SUCCESS

    def _should_retry(self, error_type: ErrorType) -> bool:
        return error_type in (
            ErrorType.SERVER_ERROR,
            ErrorType.TIMEOUT,
            ErrorType.CONNECTION_ERROR,
            ErrorType.RATE_LIMITED,
        )

    def _get_backoff_delay(self, attempt: int, error_type: ErrorType) -> float:
        if error_type == ErrorType.RATE_LIMITED:
            return min(30.0, 2.0 * (2 ** attempt))
        return min(10.0, 1.0 * (2 ** attempt))

    def _get_adaptive_timeout(self, host_state: HostState) -> float:
        if not host_state._response_times:
            return self.default_timeout
        avg = sum(host_state._response_times[-20:]) / len(host_state._response_times[-20:])
        return max(5.0, min(30.0, avg * 3.0))

    def _check_circuit(self, host_state: HostState) -> bool:
        if not host_state.circuit_open:
            return True
        elapsed = time.time() - host_state.circuit_open_time
        if elapsed >= self.circuit_timeout:
            host_state.circuit_open = False
            host_state.consecutive_failures = 0
            logger.debug(f"Circuit half-open for {host_state.host}")
            return True
        return False

    def _update_circuit(self, host_state: HostState, error_type: ErrorType):
        if error_type == ErrorType.SUCCESS:
            host_state.consecutive_failures = 0
            host_state.circuit_open = False
        elif error_type in (ErrorType.SERVER_ERROR, ErrorType.TIMEOUT, ErrorType.CONNECTION_ERROR):
            host_state.consecutive_failures += 1
            if host_state.consecutive_failures >= self.circuit_threshold:
                host_state.circuit_open = True
                host_state.circuit_open_time = time.time()
                logger.warning(f"Circuit OPEN for {host_state.host} after {host_state.consecutive_failures} failures")

    async def request(
        self,
        url: str,
        method: str = "GET",
        params: Optional[Dict] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict] = None,
        cookies: Optional[Dict] = None,
        allow_redirects: bool = False,
        timeout: Optional[float] = None,
        json_data: Optional[Dict] = None,
    ) -> Optional[RequestResult]:
        if self.is_cancelled():
            return None
        host_state = self._get_host(url)
        if not self._check_circuit(host_state):
            logger.debug(f"Circuit open for {host_state.host}, skipping")
            return RequestResult(
                status=0, body="", headers={}, url=url,
                error_type=ErrorType.CONNECTION_ERROR
            )
        now = time.time()
        elapsed = now - host_state.last_request_time
        if elapsed < host_state.delay:
            await asyncio.sleep(host_state.delay - elapsed)
        req_timeout = timeout or self._get_adaptive_timeout(host_state)
        last_error_type = ErrorType.CONNECTION_ERROR
        for attempt in range(self.max_retries + 1):
            if self.is_cancelled():
                return None
            start_time = time.time()
            try:
                import aiohttp
                kwargs = {
                    "method": method,
                    "url": url,
                    "allow_redirects": allow_redirects,
                    "timeout": aiohttp.ClientTimeout(total=req_timeout),
                    "ssl": False,
                }
                if params:
                    kwargs["params"] = params
                if data:
                    kwargs["data"] = data
                if json_data:
                    kwargs["json"] = json_data
                if headers:
                    kwargs["headers"] = headers
                if cookies:
                    kwargs["cookies"] = cookies
                async with self.session.request(**kwargs) as resp:
                    body = await resp.text()
                    resp_time = time.time() - start_time
                    resp_headers = dict(resp.headers)
                    status = resp.status
                host_state._response_times.append(resp_time)
                if len(host_state._response_times) > 50:
                    host_state._response_times = host_state._response_times[-30:]
                host_state.avg_response_time = sum(host_state._response_times) / len(host_state._response_times)
                error_type = self._classify_error(status, body)
                last_error_type = error_type
                self.total_requests += 1
                host_state.request_count += 1
                host_state.last_request_time = time.time()
                self.errors_by_type[error_type.value] = self.errors_by_type.get(error_type.value, 0) + 1
                self._update_circuit(host_state, error_type)
                if error_type == ErrorType.RATE_LIMITED:
                    retry_after = resp_headers.get("Retry-After", "")
                    if retry_after.isdigit():
                        wait = min(60.0, float(retry_after))
                    else:
                        wait = self._get_backoff_delay(attempt, error_type)
                    host_state.delay = min(5.0, host_state.delay * 2)
                    logger.debug(f"Rate limited on {host_state.host}, delay now {host_state.delay:.1f}s")
                    if attempt < self.max_retries:
                        await asyncio.sleep(wait)
                        continue
                if self._should_retry(error_type) and attempt < self.max_retries:
                    wait = self._get_backoff_delay(attempt, error_type)
                    logger.debug(f"Retry {attempt+1}/{self.max_retries} for {url} ({error_type.value}), wait {wait:.1f}s")
                    await asyncio.sleep(wait)
                    continue
                if error_type != ErrorType.SUCCESS:
                    self.total_errors += 1
                    host_state.error_count += 1
                return RequestResult(
                    status=status,
                    body=body,
                    headers=resp_headers,
                    url=str(resp.url),
                    error_type=error_type,
                    retry_count=attempt,
                    response_time=resp_time,
                )
            except asyncio.TimeoutError:
                resp_time = time.time() - start_time
                last_error_type = ErrorType.TIMEOUT
                self.total_requests += 1
                self.total_errors += 1
                host_state.request_count += 1
                host_state.error_count += 1
                host_state.last_request_time = time.time()
                self.errors_by_type["timeout"] = self.errors_by_type.get("timeout", 0) + 1
                self._update_circuit(host_state, ErrorType.TIMEOUT)
                if attempt < self.max_retries:
                    wait = self._get_backoff_delay(attempt, ErrorType.TIMEOUT)
                    logger.debug(f"Timeout on {url}, retry {attempt+1}/{self.max_retries}")
                    await asyncio.sleep(wait)
                    continue
            except Exception as e:
                resp_time = time.time() - start_time
                error_type = self._classify_error(0, "", e)
                last_error_type = error_type
                self.total_requests += 1
                self.total_errors += 1
                host_state.request_count += 1
                host_state.error_count += 1
                host_state.last_request_time = time.time()
                self.errors_by_type[error_type.value] = self.errors_by_type.get(error_type.value, 0) + 1
                self._update_circuit(host_state, error_type)
                if self._should_retry(error_type) and attempt < self.max_retries:
                    wait = self._get_backoff_delay(attempt, error_type)
                    logger.debug(f"Error on {url}: {e}, retry {attempt+1}")
                    await asyncio.sleep(wait)
                    continue
                logger.debug(f"Request failed after {attempt+1} attempts: {url} - {e}")
        return RequestResult(
            status=0, body="", headers={}, url=url,
            error_type=last_error_type, retry_count=self.max_retries,
        )

    def get_stats(self) -> Dict:
        host_stats = {}
        for host, state in self._hosts.items():
            host_stats[host] = {
                "requests": state.request_count,
                "errors": state.error_count,
                "avg_response_time": round(state.avg_response_time, 3),
                "delay": round(state.delay, 3),
                "circuit_open": state.circuit_open,
                "consecutive_failures": state.consecutive_failures,
            }
        return {
            "total_requests": self.total_requests,
            "total_errors": self.total_errors,
            "errors_by_type": dict(self.errors_by_type),
            "hosts": host_stats,
        }

    def reset_stats(self):
        self.total_requests = 0
        self.total_errors = 0
        self.errors_by_type = {e.value: 0 for e in ErrorType}
        self._hosts.clear()