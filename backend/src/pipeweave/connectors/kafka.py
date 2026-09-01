"""Kafka Connector"""
from .base import BaseSourceConnector, BaseSinkConnector
from ..core.types import RecordBatch

class KafkaSourceConnector(BaseSourceConnector):
    async def connect(self): self.is_connected = True
    async def disconnect(self): self.is_connected = False
    async def read_batch(self, limit=None):
        cnt = limit or 500
        records = [{"event_id": f"evt_{i}", "topic": self.config.topic, "amount": float(i * 5.5)} for i in range(1, cnt + 1)]
        return RecordBatch(records=records, metadata={"source": "Kafka"})

class KafkaSinkConnector(BaseSinkConnector):
    async def connect(self): self.is_connected = True
    async def disconnect(self): self.is_connected = False
    async def write_batch(self, batch: RecordBatch): return len(batch.records)
