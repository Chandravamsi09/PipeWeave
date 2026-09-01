"""Data Quality Engine"""
from typing import List, Optional
from dataclasses import dataclass
from ..core.types import RecordBatch, QualityCheckResult

@dataclass
class ExpectationRule:
    rule_type: str
    column: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    severity: str = "FAIL_PIPELINE"

class DataQualityEngine:
    def __init__(self, rules=None): self.rules = rules or []
    def evaluate(self, batch: RecordBatch) -> List[QualityCheckResult]:
        results = []
        for rule in self.rules:
            if rule.rule_type == "NOT_NULL" and rule.column:
                nulls = sum(1 for r in batch.records if r.get(rule.column) is None)
                results.append(QualityCheckResult("expect_not_null", rule.column, (nulls == 0), nulls, 0, nulls, rule.severity))
            elif rule.rule_type == "IN_RANGE" and rule.column:
                out_b = sum(1 for r in batch.records if isinstance(r.get(rule.column), (int, float)) and ((rule.min_value is not None and r[rule.column] < rule.min_value) or (rule.max_value is not None and r[rule.column] > rule.max_value)))
                results.append(QualityCheckResult("expect_in_range", rule.column, (out_b == 0), out_b, 0, out_b, rule.severity))
            elif rule.rule_type == "MIN_ROW_COUNT":
                min_c = int(rule.min_value or 1)
                results.append(QualityCheckResult("expect_min_rows", None, (batch.row_count >= min_c), batch.row_count, min_c, 0, rule.severity))
        return results
