"""Connector Base Interfaces"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from ..core.types import RecordBatch

@dataclass
class ConnectorConfig:
    connector_type: str
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None
    table_name: Optional[str] = None
    topic: Optional[str] = None
    bucket: Optional[str] = None
    path: Optional[str] = None
    batch_size: int = 10000
    options: Dict[str, Any] = field(default_factory=dict)

class BaseSourceConnector(ABC):
    def __init__(self, config: ConnectorConfig): self.config = config; self.is_connected = False
    @abstractmethod
    async def connect(self): pass
    @abstractmethod
    async def disconnect(self): pass
    @abstractmethod
    async def read_batch(self, limit: Optional[int] = None) -> RecordBatch: pass

class BaseSinkConnector(ABC):
    def __init__(self, config: ConnectorConfig): self.config = config; self.is_connected = False
    @abstractmethod
    async def connect(self): pass
    @abstractmethod
    async def disconnect(self): pass
    @abstractmethod
    async def write_batch(self, batch: RecordBatch) -> int: pass
