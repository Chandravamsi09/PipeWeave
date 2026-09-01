"""Execution Context"""
from typing import Dict, Any, Optional
from datetime import datetime
from ..core.types import RecordBatch

class ExecutionContext:
    def __init__(self, pipeline_id: str, run_id: str, task_id: str, node_key: str, config: Optional[Dict[str, Any]] = None):
        self.pipeline_id = pipeline_id
        self.run_id = run_id
        self.task_id = task_id
        self.node_key = node_key
        self.config = config or {}
        self.start_time = datetime.utcnow()
        self.xcom: Dict[str, Any] = {}
        self.input_batch: Optional[RecordBatch] = None
        self.output_batch: Optional[RecordBatch] = None
        self.logs: list[str] = []

    def log(self, msg: str): self.logs.append(f"[{datetime.utcnow().isoformat()}] {msg}")
    def set_xcom(self, k: str, v: Any): self.xcom[k] = v
    def get_xcom(self, k: str, default: Any = None): return self.xcom.get(k, default)
