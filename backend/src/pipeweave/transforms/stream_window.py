"""Stream Windowing Engine"""
import time
from datetime import datetime
from .base import BaseTransform, TransformResult
from ..core.types import RecordBatch

class StreamWindowEngine(BaseTransform):
    def __init__(self, size_seconds: int = 60, agg_field: str = "amount"):
        super().__init__()
        self.size_seconds = size_seconds
        self.agg_field = agg_field

    def execute(self, batch: RecordBatch) -> TransformResult:
        start = time.time()
        records = batch.records
        total = sum(float(r.get(self.agg_field, 0)) for r in records)
        count = len(records)
        avg = total / count if count > 0 else 0.0
        out_row = {"window_size_sec": self.size_seconds, "event_count": count, f"total_{self.agg_field}": total, f"avg_{self.agg_field}": round(avg, 4), "timestamp": datetime.utcnow().isoformat()}
        return TransformResult(output_batch=RecordBatch(records=[out_row]), rows_in=count, rows_out=1, duration_ms=(time.time() - start) * 1000.0)
