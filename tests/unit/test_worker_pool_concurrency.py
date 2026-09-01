"""Test Worker Concurrency"""
import asyncio
from pipeweave.engine.executor import WorkerPool

def test_worker_concurrency():
    async def _test():
        pool = WorkerPool(max_concurrency=2)
        active, max_active = 0, 0
        async def work():
            nonlocal active, max_active
            active += 1
            max_active = max(max_active, active)
            await asyncio.sleep(0.01)
            active -= 1
        await asyncio.gather(*[pool.submit(f"t_{i}", work()) for i in range(4)])
        assert max_active <= 2
    asyncio.run(_test())
