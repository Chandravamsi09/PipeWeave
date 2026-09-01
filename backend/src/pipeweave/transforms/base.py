"""Transforms Base"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
from ..core.types import RecordBatch

@dataclass
class TransformResult:
    output_batch: RecordBatch
    rows_in: int
    rows_out: int
    duration_ms: float = 0.0

class BaseTransform(ABC):
    def __init__(self, config=None): self.config = config or {}
    @abstractmethod
    def execute(self, batch: RecordBatch) -> TransformResult: pass
