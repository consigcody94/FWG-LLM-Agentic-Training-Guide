"""
Production Reliability Patterns - Reference Implementation

This module provides production-ready reliability patterns for
AI agent systems, including circuit breakers, retry mechanisms,
fallback chains, and health monitoring.

Part of Module 28: Antigravity - Advanced Agent Techniques
"""

from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from functools import wraps
import asyncio
import random
import time
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


T = TypeVar('T')


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, rejecting calls
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitStats:
    """Statistics for circuit breaker monitoring."""
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    rejected_calls: int = 0
    last_failure_time: Optional[datetime] = None
    last_success_time: Optional[datetime] = None
    state_changes: List[Tuple[datetime, CircuitState]] = field(
        default_factory=list
    )

    @property
    def success_rate(self) -> float:
        if self.total_calls == 0:
            return 1.0
        return self.successful_calls / self.total_calls

    @property
    def failure_rate(self) -> float:
        if self.total_calls == 0:
            return 0.0
        return self.failed_calls / self.total_calls


class CircuitBreaker:
    """
    Circuit breaker pattern for fault tolerance.

    Prevents cascading failures by stopping calls to a failing
    service and allowing it time to recover.

    States:
        CLOSED: Normal operation, calls pass through
        OPEN: Service failing, calls rejected immediately
        HALF_OPEN: Testing recovery, limited calls allowed

    Example:
        breaker = CircuitBreaker(failure_threshold=5)

        @breaker
        async def call_api():
            return await some_api_call()
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        half_open_max_calls: int = 3,
        failure_rate_threshold: float = 0.5,
        min_calls_for_rate: int = 10
    ):
        """
        Initialize circuit breaker.

        Args:
            failure_threshold: Consecutive failures before opening
            recovery_timeout: Seconds before trying recovery
            half_open_max_calls: Max calls in half-open state
            failure_rate_threshold: Failure rate to trigger open
            min_calls_for_rate: Minimum calls before rate check
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        self.failure_rate_threshold = failure_rate_threshold
        self.min_calls_for_rate = min_calls_for_rate

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._half_open_calls = 0
        self._last_failure_time: Optional[datetime] = None

        self.stats = CircuitStats()

    @property
    def state(self) -> CircuitState:
        """Get current circuit state."""
        self._check_state_transition()
        return self._state

    def _check_state_transition(self):
        """Check if state should transition."""
        if self._state == CircuitState.OPEN:
            if self._last_failure_time:
                elapsed = (
                    datetime.now() - self._last_failure_time
                ).total_seconds()
                if elapsed >= self.recovery_timeout:
                    self._transition_to(CircuitState.HALF_OPEN)

    def _transition_to(self, new_state: CircuitState):
        """Transition to a new state."""
        if new_state != self._state:
            logger.info(
                f"Circuit breaker: {self._state.value} -> {new_state.value}"
            )
            self._state = new_state
            self.stats.state_changes.append((datetime.now(), new_state))

            if new_state == CircuitState.HALF_OPEN:
                self._half_open_calls = 0
            elif new_state == CircuitState.CLOSED:
                self._failure_count = 0

    def _record_success(self):
        """Record successful call."""
        self.stats.total_calls += 1
        self.stats.successful_calls += 1
        self.stats.last_success_time = datetime.now()

        if self._state == CircuitState.HALF_OPEN:
            self._half_open_calls += 1
            if self._half_open_calls >= self.half_open_max_calls:
                self._transition_to(CircuitState.CLOSED)

        self._failure_count = 0

    def _record_failure(self, error: Exception):
        """Record failed call."""
        self.stats.total_calls += 1
        self.stats.failed_calls += 1
        self.stats.last_failure_time = datetime.now()
        self._last_failure_time = datetime.now()

        self._failure_count += 1

        # Check if should open
        should_open = False

        if self._failure_count >= self.failure_threshold:
            should_open = True

        if (self.stats.total_calls >= self.min_calls_for_rate and
            self.stats.failure_rate >= self.failure_rate_threshold):
            should_open = True

        if should_open:
            self._transition_to(CircuitState.OPEN)
        elif self._state == CircuitState.HALF_OPEN:
            self._transition_to(CircuitState.OPEN)

    def _can_execute(self) -> bool:
        """Check if call can be executed."""
        state = self.state  # Triggers state check

        if state == CircuitState.CLOSED:
            return True
        elif state == CircuitState.OPEN:
            self.stats.rejected_calls += 1
            return False
        else:  # HALF_OPEN
            return self._half_open_calls < self.half_open_max_calls

    def __call__(self, func: Callable) -> Callable:
        """Decorator to wrap function with circuit breaker."""
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            if not self._can_execute():
                raise CircuitOpenError(
                    f"Circuit breaker is {self._state.value}"
                )

            try:
                result = await func(*args, **kwargs)
                self._record_success()
                return result
            except Exception as e:
                self._record_failure(e)
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            if not self._can_execute():
                raise CircuitOpenError(
                    f"Circuit breaker is {self._state.value}"
                )

            try:
                result = func(*args, **kwargs)
                self._record_success()
                return result
            except Exception as e:
                self._record_failure(e)
                raise

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    def reset(self):
        """Manually reset the circuit breaker."""
        self._transition_to(CircuitState.CLOSED)
        self._failure_count = 0
        self._last_failure_time = None


class CircuitOpenError(Exception):
    """Raised when circuit breaker is open."""
    pass


class RetryStrategy(Enum):
    """Retry backoff strategies."""
    CONSTANT = "constant"
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    EXPONENTIAL_JITTER = "exponential_jitter"


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_JITTER
    retryable_exceptions: Tuple[type, ...] = (Exception,)

    def get_delay(self, attempt: int) -> float:
        """Calculate delay for an attempt."""
        if self.strategy == RetryStrategy.CONSTANT:
            delay = self.base_delay
        elif self.strategy == RetryStrategy.LINEAR:
            delay = self.base_delay * attempt
        elif self.strategy == RetryStrategy.EXPONENTIAL:
            delay = self.base_delay * (2 ** (attempt - 1))
        else:  # EXPONENTIAL_JITTER
            delay = self.base_delay * (2 ** (attempt - 1))
            jitter = random.uniform(0, delay * 0.1)
            delay += jitter

        return min(delay, self.max_delay)


def retry_with_backoff(config: RetryConfig = None):
    """
    Decorator for retrying failed operations with backoff.

    Args:
        config: Retry configuration

    Example:
        @retry_with_backoff(RetryConfig(max_retries=3))
        async def flaky_operation():
            ...
    """
    config = config or RetryConfig()

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, config.max_retries + 2):
                try:
                    return await func(*args, **kwargs)
                except config.retryable_exceptions as e:
                    last_exception = e

                    if attempt > config.max_retries:
                        break

                    delay = config.get_delay(attempt)
                    logger.warning(
                        f"Attempt {attempt} failed: {e}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    await asyncio.sleep(delay)

            raise last_exception

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, config.max_retries + 2):
                try:
                    return func(*args, **kwargs)
                except config.retryable_exceptions as e:
                    last_exception = e

                    if attempt > config.max_retries:
                        break

                    delay = config.get_delay(attempt)
                    logger.warning(
                        f"Attempt {attempt} failed: {e}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    time.sleep(delay)

            raise last_exception

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator


@dataclass
class FallbackOption:
    """A fallback option in the chain."""
    name: str
    handler: Callable
    priority: int = 0
    is_available: Callable[[], bool] = lambda: True


class FallbackChain:
    """
    Fallback chain for graceful degradation.

    Tries primary option first, then falls back to
    alternatives in priority order.

    Example:
        chain = FallbackChain()
        chain.add("primary", primary_handler, priority=0)
        chain.add("backup", backup_handler, priority=1)
        chain.add("cache", cache_handler, priority=2)

        result = await chain.execute(task)
    """

    def __init__(self):
        self.options: List[FallbackOption] = []

    def add(
        self,
        name: str,
        handler: Callable,
        priority: int = None,
        is_available: Callable[[], bool] = None
    ):
        """Add a fallback option."""
        if priority is None:
            priority = len(self.options)

        option = FallbackOption(
            name=name,
            handler=handler,
            priority=priority,
            is_available=is_available or (lambda: True)
        )

        self.options.append(option)
        self.options.sort(key=lambda x: x.priority)

    async def execute(
        self,
        *args,
        **kwargs
    ) -> Tuple[Any, str]:
        """
        Execute with fallback chain.

        Returns:
            Tuple of (result, handler_name)
        """
        errors = []

        for option in self.options:
            if not option.is_available():
                continue

            try:
                if asyncio.iscoroutinefunction(option.handler):
                    result = await option.handler(*args, **kwargs)
                else:
                    result = option.handler(*args, **kwargs)

                logger.info(f"Fallback chain: {option.name} succeeded")
                return result, option.name

            except Exception as e:
                errors.append((option.name, e))
                logger.warning(
                    f"Fallback chain: {option.name} failed: {e}"
                )

        raise FallbackExhaustedError(
            f"All fallback options exhausted. Errors: {errors}"
        )


class FallbackExhaustedError(Exception):
    """Raised when all fallback options fail."""
    pass


class RateLimiter:
    """
    Rate limiter using token bucket algorithm.

    Controls the rate of operations to prevent
    overwhelming downstream services.

    Example:
        limiter = RateLimiter(rate=10, capacity=20)

        @limiter
        async def api_call():
            ...
    """

    def __init__(
        self,
        rate: float,
        capacity: float = None
    ):
        """
        Initialize rate limiter.

        Args:
            rate: Tokens per second
            capacity: Maximum bucket capacity
        """
        self.rate = rate
        self.capacity = capacity or rate * 2
        self.tokens = self.capacity
        self.last_update = time.time()
        self._lock = asyncio.Lock()

    async def acquire(self, tokens: float = 1.0) -> float:
        """
        Acquire tokens, waiting if necessary.

        Returns wait time in seconds.
        """
        async with self._lock:
            # Refill tokens
            now = time.time()
            elapsed = now - self.last_update
            self.tokens = min(
                self.capacity,
                self.tokens + elapsed * self.rate
            )
            self.last_update = now

            # Check if tokens available
            if self.tokens >= tokens:
                self.tokens -= tokens
                return 0.0

            # Calculate wait time
            needed = tokens - self.tokens
            wait_time = needed / self.rate

            await asyncio.sleep(wait_time)
            self.tokens = 0
            self.last_update = time.time()

            return wait_time

    def __call__(self, func: Callable) -> Callable:
        """Decorator to rate limit a function."""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            await self.acquire()
            return await func(*args, **kwargs)
        return wrapper


@dataclass
class HealthStatus:
    """Health status of a component."""
    name: str
    healthy: bool
    last_check: datetime
    details: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


class HealthMonitor:
    """
    Health monitoring for agent components.

    Tracks health of various components and provides
    aggregated health status.

    Example:
        monitor = HealthMonitor()
        monitor.register("llm_api", llm_health_check)
        monitor.register("database", db_health_check)

        status = await monitor.check_all()
    """

    def __init__(self, check_interval: float = 30.0):
        self.check_interval = check_interval
        self.checks: Dict[str, Callable] = {}
        self.status: Dict[str, HealthStatus] = {}
        self._running = False

    def register(
        self,
        name: str,
        check_fn: Callable[[], bool]
    ):
        """Register a health check."""
        self.checks[name] = check_fn

    async def check(self, name: str) -> HealthStatus:
        """Run a single health check."""
        if name not in self.checks:
            raise ValueError(f"Unknown check: {name}")

        check_fn = self.checks[name]

        try:
            if asyncio.iscoroutinefunction(check_fn):
                result = await check_fn()
            else:
                result = check_fn()

            status = HealthStatus(
                name=name,
                healthy=bool(result),
                last_check=datetime.now(),
                details=result if isinstance(result, dict) else {}
            )
        except Exception as e:
            status = HealthStatus(
                name=name,
                healthy=False,
                last_check=datetime.now(),
                error=str(e)
            )

        self.status[name] = status
        return status

    async def check_all(self) -> Dict[str, HealthStatus]:
        """Run all health checks."""
        tasks = [self.check(name) for name in self.checks]
        await asyncio.gather(*tasks)
        return self.status.copy()

    def is_healthy(self) -> bool:
        """Check if all components are healthy."""
        if not self.status:
            return True
        return all(s.healthy for s in self.status.values())

    async def start_monitoring(self):
        """Start continuous health monitoring."""
        self._running = True
        while self._running:
            await self.check_all()
            await asyncio.sleep(self.check_interval)

    def stop_monitoring(self):
        """Stop continuous monitoring."""
        self._running = False


class Timeout:
    """
    Timeout wrapper for operations.

    Example:
        @Timeout(seconds=30)
        async def slow_operation():
            ...
    """

    def __init__(self, seconds: float):
        self.seconds = seconds

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(
                    func(*args, **kwargs),
                    timeout=self.seconds
                )
            except asyncio.TimeoutError:
                raise TimeoutError(
                    f"Operation timed out after {self.seconds}s"
                )
        return wrapper


class BulkheadLimiter:
    """
    Bulkhead pattern for isolation.

    Limits concurrent executions to prevent one component
    from consuming all resources.

    Example:
        bulkhead = BulkheadLimiter(max_concurrent=10)

        @bulkhead
        async def resource_intensive():
            ...
    """

    def __init__(self, max_concurrent: int = 10):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.active = 0
        self.rejected = 0

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if self.semaphore.locked():
                self.rejected += 1
                raise BulkheadFullError(
                    f"Bulkhead at capacity ({self.max_concurrent})"
                )

            async with self.semaphore:
                self.active += 1
                try:
                    return await func(*args, **kwargs)
                finally:
                    self.active -= 1

        return wrapper

    def get_stats(self) -> Dict[str, int]:
        return {
            "max_concurrent": self.max_concurrent,
            "active": self.active,
            "rejected": self.rejected
        }


class BulkheadFullError(Exception):
    """Raised when bulkhead is at capacity."""
    pass


# Convenience function to create a resilient wrapper
def resilient(
    circuit_breaker: CircuitBreaker = None,
    retry_config: RetryConfig = None,
    rate_limiter: RateLimiter = None,
    timeout_seconds: float = None
):
    """
    Combine multiple reliability patterns.

    Example:
        @resilient(
            circuit_breaker=CircuitBreaker(),
            retry_config=RetryConfig(max_retries=3),
            timeout_seconds=30
        )
        async def critical_operation():
            ...
    """
    def decorator(func: Callable) -> Callable:
        wrapped = func

        # Apply in reverse order (innermost first)
        if timeout_seconds:
            wrapped = Timeout(timeout_seconds)(wrapped)

        if retry_config:
            wrapped = retry_with_backoff(retry_config)(wrapped)

        if circuit_breaker:
            wrapped = circuit_breaker(wrapped)

        if rate_limiter:
            wrapped = rate_limiter(wrapped)

        return wrapped

    return decorator


# Example usage
if __name__ == "__main__":
    async def demo():
        # Circuit breaker demo
        print("=== Circuit Breaker Demo ===")
        breaker = CircuitBreaker(failure_threshold=3)

        @breaker
        async def flaky_service():
            if random.random() < 0.7:
                raise Exception("Service error")
            return "Success"

        for i in range(10):
            try:
                result = await flaky_service()
                print(f"Call {i+1}: {result}")
            except CircuitOpenError as e:
                print(f"Call {i+1}: Circuit open - {e}")
            except Exception as e:
                print(f"Call {i+1}: Failed - {e}")

        print(f"Stats: {breaker.stats.success_rate:.1%} success rate")

        # Retry demo
        print("\n=== Retry Demo ===")
        call_count = 0

        @retry_with_backoff(RetryConfig(
            max_retries=3,
            base_delay=0.1,
            strategy=RetryStrategy.EXPONENTIAL_JITTER
        ))
        async def eventually_succeeds():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception("Not yet")
            return "Finally worked!"

        result = await eventually_succeeds()
        print(f"Result: {result} (took {call_count} attempts)")

        # Fallback chain demo
        print("\n=== Fallback Chain Demo ===")
        chain = FallbackChain()

        async def primary_fails():
            raise Exception("Primary failed")

        async def backup_succeeds():
            return "Backup result"

        chain.add("primary", primary_fails, priority=0)
        chain.add("backup", backup_succeeds, priority=1)

        result, handler = await chain.execute()
        print(f"Result: {result} (from {handler})")

        # Rate limiter demo
        print("\n=== Rate Limiter Demo ===")
        limiter = RateLimiter(rate=5, capacity=5)

        @limiter
        async def limited_call():
            return "Done"

        start = time.time()
        for i in range(10):
            await limited_call()
        elapsed = time.time() - start
        print(f"10 calls took {elapsed:.2f}s (rate limited to 5/s)")

        print("\nDemo complete!")

    asyncio.run(demo())
