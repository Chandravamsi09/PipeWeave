"""Dataset Profiler"""
from dataclasses import dataclass
from ..core.types import RecordBatch

@dataclass
class ColumnProfile:
    column_name: str
    total_count: int
    null_count: int
    distinct_count: int
    mean_value: float = 0.0

class DatasetProfiler:
    @staticmethod
    def profile_batch(batch: RecordBatch):
        if not batch.records: return {}
        cols = list(batch.records[0].keys())
        return {c: ColumnProfile(c, batch.row_count, 0, len(set(r.get(c) for r in batch.records))) for c in cols}
