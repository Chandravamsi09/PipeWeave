"""E2E Pipeline Test"""
import asyncio
from pipeweave.engine.graph import DAG, DAGNode
from pipeweave.engine.scheduler import DAGScheduler
from pipeweave.core.types import RecordBatch
from pipeweave.core.constants import PipelineState

def test_full_pipeline_e2e():
    async def _test():
        dag = DAG(name="E2EPipeline")
        dag.add_node(DAGNode("src", "Source", "SOURCE"))
        dag.add_node(DAGNode("clean", "Clean", "TRANSFORM"))
        dag.add_node(DAGNode("sink", "Sink", "SINK"))
        dag.add_edge("src", "clean")
        dag.add_edge("clean", "sink")
        async def src_h(ctx): return RecordBatch(records=[{"id": 1, "amount": 100}, {"id": 2, "amount": 200}])
        async def clean_h(ctx): return RecordBatch(records=[{**r, "clean": True} for r in ctx.input_batch.records])
        async def sink_h(ctx): return ctx.input_batch
        scheduler = DAGScheduler()
        plan = await scheduler.run_pipeline("test-pipe", dag, {"src": src_h, "clean": clean_h, "sink": sink_h})
        assert plan.state == PipelineState.SUCCESS
        assert len(plan.node_outputs["sink"].records) == 2
    asyncio.run(_test())
