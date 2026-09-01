"""Test Retry Policy"""
import asyncio
from pipeweave.engine.retry import RetryPolicy, CircuitBreaker

def test_retry_policy():
    async def _test():
        c = 0
        async def flaky():
            nonlocal c
            c += 1
            if c < 3: raise ValueError("error")
            return "ok"
        p = RetryPolicy(max_attempts=4, initial_delay_seconds=0.01)
        res = await p.execute_with_retry(flaky)
        assert res == "ok"
        assert c == 3
    asyncio.run(_test())
