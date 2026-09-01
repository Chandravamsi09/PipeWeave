"""Worker Execution Pool"""
import asyncio
from concurrent.futures import ThreadPoolExecutor
from ..core.exceptions import TaskExecutionError
from .context import ExecutionContext
from .retry import RetryPolicy

class TaskExecutor:
    def __init__(self, node_key: str, handler):
        self.node_key = node_key
        self.handler = handler

    async def run(self, context: ExecutionContext, retry_policy=None):
        policy = retry_policy or RetryPolicy(max_attempts=1)
        async def _inv():
            return await self.handler(context)
        return await policy.execute_with_retry(_inv)

class WorkerPool:
    def __init__(self, max_concurrency: int = 16, max_threads: int = 8):
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.pool = ThreadPoolExecutor(max_workers=max_threads)

    async def submit(self, task_id: str, coro):
        async with self.semaphore: return await coro

    async def run_in_thread(self, func, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.pool, lambda: func(*args, **kwargs))

    def shutdown(self): self.pool.shutdown(wait=False)
