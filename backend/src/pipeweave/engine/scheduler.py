"""DAG Scheduler"""
import asyncio
from datetime import datetime
import uuid
from .graph import DAG
from .context import ExecutionContext
from .executor import WorkerPool, TaskExecutor
from .retry import RetryPolicy
from ..core.constants import TaskState, PipelineState
from ..core.events import event_bus
from ..core.types import RecordBatch

class PipelineExecutionPlan:
    def __init__(self, run_id: str, dag: DAG):
        self.run_id = run_id
        self.dag = dag
        self.state = PipelineState.RUNNING
        self.task_states = {k: TaskState.PENDING for k in dag.nodes.keys()}
        self.node_outputs = {}
        self.started_at = datetime.utcnow()
        self.finished_at = None

class DAGScheduler:
    def __init__(self, worker_pool=None):
        self.worker_pool = worker_pool or WorkerPool()

    async def run_pipeline(self, pipeline_id: str, dag: DAG, handlers, initial_input=None):
        dag.validate()
        run_id = str(uuid.uuid4())
        plan = PipelineExecutionPlan(run_id, dag)
        tiers = dag.compute_execution_tiers()
        for tier_nodes in tiers:
            tier_tasks = [self._exec_node(pipeline_id, plan, k, handlers.get(k), initial_input) for k in tier_nodes]
            results = await asyncio.gather(*tier_tasks, return_exceptions=True)
            for k, res in zip(tier_nodes, results):
                if isinstance(res, Exception):
                    plan.state = PipelineState.FAILED
                    raise res
        plan.state = PipelineState.SUCCESS
        plan.finished_at = datetime.utcnow()
        return plan

    async def _exec_node(self, pipeline_id, plan, node_key, handler, initial_input):
        node = plan.dag.nodes[node_key]
        ctx = ExecutionContext(pipeline_id, plan.run_id, str(uuid.uuid4()), node_key, node.config)
        upstreams = plan.dag.get_upstream_nodes(node_key)
        ctx.input_batch = plan.node_outputs.get(upstreams[0]) if upstreams else initial_input
        async def _work(c):
            if handler:
                return await handler(c) if asyncio.iscoroutinefunction(handler) else await self.worker_pool.run_in_thread(handler, c)
            return c.input_batch
        executor = TaskExecutor(node_key, _work)
        out = await self.worker_pool.submit(ctx.task_id, executor.run(ctx))
        plan.node_outputs[node_key] = out
        plan.task_states[node_key] = TaskState.SUCCESS
        return out
