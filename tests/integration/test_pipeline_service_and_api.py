"""Integration Test for Real Pipeline Execution & APIs"""
import asyncio
from pipeweave.services.pipeline_service import PipelineExecutionService
from pipeweave.core.db import RunRepository, SchemaRepository

def test_pipeline_execution_service():
    async def _test():
        result = await PipelineExecutionService.execute_pipeline("pipe-ecom")
        assert result["state"] == "SUCCESS"
        assert result["records_processed"] == 1000
        assert result["duration_ms"] > 0
        assert "revenue_agg" in result["node_outputs"]
        
        # Verify persistence in SQLite
        runs = RunRepository.list_all(limit=5)
        assert len(runs) > 0
        latest_run = runs[0]
        assert latest_run["pipeline_id"] == "pipe-ecom"
        assert latest_run["records_processed"] == 1000
    
    asyncio.run(_test())

def test_schema_persistence():
    test_subject = "orders-integration-test"
    SchemaRepository.save(
        subject=test_subject,
        version=1,
        schema_type="AVRO",
        schema_def={"type": "record", "name": "TestEvent", "fields": [{"name": "id", "type": "string"}]}
    )
    all_schemas = SchemaRepository.list_all()
    found = [s for s in all_schemas if s["subject"] == test_subject]
    assert len(found) == 1
    assert found[0]["version"] == 1
