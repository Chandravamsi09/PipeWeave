"""Domain Data Types & Structures"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class RecordBatch:
    batch_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    records: List[Dict[str, Any]] = field(default_factory=list)
    schema_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    row_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.row_count and self.records:
            self.row_count = len(self.records)

    def append(self, record: Dict[str, Any]) -> None:
        self.records.append(record)
        self.row_count += 1

    def extend(self, records: List[Dict[str, Any]]) -> None:
        self.records.extend(records)
        self.row_count += len(records)

@dataclass
class QualityCheckResult:
    rule_name: str
    column: Optional[str]
    passed: bool
    observed_value: Any
    expected_value: Any
    failed_records_count: int = 0
    severity: str = "FAIL_PIPELINE"
    message: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
