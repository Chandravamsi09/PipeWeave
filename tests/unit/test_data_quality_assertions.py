"""Test Quality Assertions"""
from pipeweave.quality.assertions import DataQualityEngine, ExpectationRule
from pipeweave.core.types import RecordBatch

def test_quality_assertions():
    engine = DataQualityEngine([
        ExpectationRule(rule_type="NOT_NULL", column="id"),
        ExpectationRule(rule_type="IN_RANGE", column="amount", min_value=0.0, max_value=1000.0),
        ExpectationRule(rule_type="MIN_ROW_COUNT", min_value=2),
    ])
    batch = RecordBatch(records=[{"id": "1", "amount": 100.0}, {"id": "2", "amount": 250.0}])
    results = engine.evaluate(batch)
    assert len(results) == 3
    assert all(r.passed for r in results)
