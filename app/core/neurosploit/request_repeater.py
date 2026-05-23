import asyncio
import logging
from typing import Callable, Optional, Any

logger = logging.getLogger(__name__)


class RequestRepeater:

    RETRYABLE_ERRORS = frozenset({
        "server_error", "timeout", "connection_error", "rate_limited",
    })

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        multiplier: float = 2.0,
        jitter: float = 0.5,
        is_cancelled_fn: Optional[Callable] = None,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.multiplier = multiplier
        self.jitter = jitter
        self.is_cancelled = is_cancelled_fn or (lambda: False)

    def _calc_delay(self, attempt: int, error_type: str) -> float:
        delay = self.base_delay * (self.multiplier ** attempt)
        if error_type == "rate_limited":
            delay *= 2
        delay = min(delay, self.max_delay)
        if self.jitter > 0:
            import random
            jitter_amount = delay * self.jitter
            delay += random.uniform(-jitter_amount, jitter_amount)
        return max(0.1, delay)

    async def execute_with_retry(
        self,
        fn: Callable,
        *args,
        classify_fn: Optional[Callable[[Any], str]] = None,
        should_retry_fn: Optional[Callable[[str], bool]] = None,
        **kwargs,
    ) -> tuple[bool, Any]:
        last_result = None
        last_error_type = "unknown"
        for attempt in range(self.max_retries + 1):
            if self.is_cancelled():
                return False, None
            try:
                result = await fn(*args, **kwargs)
                error_type = "success"
                if classify_fn:
                    error_type = classify_fn(result)
                last_result = result
                last_error_type = error_type
                if error_type == "success":
                    return True, result
                retry_fn = should_retry_fn or (lambda et: et in self.RETRYABLE_ERRORS)
                if retry_fn(error_type) and attempt < self.max_retries:
                    delay = self._calc_delay(attempt, error_type)
                    logger.debug(f"Retry {attempt+1}/{self.max_retries} ({error_type}), delay {delay:.1f}s")
                    await asyncio.sleep(delay)
                    continue
                return False, result
            except asyncio.TimeoutError:
                last_error_type = "timeout"
                if attempt < self.max_retries:
                    delay = self._calc_delay(attempt, "timeout")
                    logger.debug(f"Timeout, retry {attempt+1}/{self.max_retries}, delay {delay:.1f}s")
                    await asyncio.sleep(delay)
                    continue
                return False, None
            except Exception as e:
                last_error_type = "connection_error"
                if attempt < self.max_retries:
                    delay = self._calc_delay(attempt, "connection_error")
                    logger.debug(f"Error: {e}, retry {attempt+1}/{self.max_retries}")
                    await asyncio.sleep(delay)
                    continue
                return False, None
        return False, last_result

    async def execute_once(self, fn: Callable, *args, **kwargs) -> tuple[bool, Any]:
        try:
            result = await fn(*args, **kwargs)
            return True, result
        except Exception as e:
            logger.debug(f"Execute once failed: {e}")
            return False, None