"""Retry and Fault Tolerance"""
import asyncio
import time
import logging

class RetryPolicy:
    def __init__(self, max_attempts: int = 3, initial_delay_seconds: float = 1.0):
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay_seconds

    async def execute_with_retry(self, func, *args, **kwargs):
        attempt = 1
        while True:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if attempt >= self.max_attempts: raise e
                await asyncio.sleep(self.initial_delay * attempt)
                attempt += 1

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout_seconds: float = 30.0):
        self.threshold = failure_threshold
        self.recovery_timeout = recovery_timeout_seconds
        self.failures = 0
        self.last_failure = 0.0
        self.state = "CLOSED"

    def record_success(self): self.failures = 0; self.state = "CLOSED"
    def record_failure(self):
        self.failures += 1; self.last_failure = time.time()
        if self.failures >= self.threshold: self.state = "OPEN"
    def allow_request(self) -> bool:
        if self.state == "CLOSED": return True
        if self.state == "OPEN":
            if time.time() - self.last_failure > self.recovery_timeout:
                self.state = "HALF_OPEN"; return True
            return False
        return True
