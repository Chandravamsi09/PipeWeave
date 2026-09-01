"""Test Stream Windowing"""
from pipeweave.transforms.stream_window import StreamWindowEngine
from pipeweave.core.types import RecordBatch

def test_stream_window_aggregate():
    engine = StreamWindowEngine(size_seconds=60, agg_field="amount")
    batch = RecordBatch(records=[{"id": 1, "amount": 100.0}, {"id": 2, "amount": 200.0}])
    res = engine.execute(batch)
    assert res.rows_out == 1
    assert res.output_batch.records[0]["total_amount"] == 300.0
