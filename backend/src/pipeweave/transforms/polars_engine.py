"""Polars Transform Engine"""
import time
from .base import BaseTransform, TransformResult
from ..core.types import RecordBatch

class PolarsTransformEngine(BaseTransform):
    def __init__(self, group_by_col=None, agg_col=None):
        super().__init__()
        self.group_by_col = group_by_col
        self.agg_col = agg_col

    def execute(self, batch: RecordBatch) -> TransformResult:
        start = time.time()
        records = batch.records
        if self.group_by_col and self.agg_col and records:
            groups = {}
            for r in records:
                k = r.get(self.group_by_col)
                val = float(r.get(self.agg_col, 0))
                groups[k] = groups.get(k, 0.0) + val
            out_records = [{self.group_by_col: k, f"sum_{self.agg_col}": v} for k, v in groups.items()]
        else:
            out_records = records
        return TransformResult(output_batch=RecordBatch(records=out_records), rows_in=len(records), rows_out=len(out_records), duration_ms=(time.time() - start) * 1000.0)
