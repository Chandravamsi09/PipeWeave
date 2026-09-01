"""PostgreSQL Connector"""
from .base import BaseSourceConnector, BaseSinkConnector
from ..core.types import RecordBatch

class PostgresSourceConnector(BaseSourceConnector):
    async def connect(self): self.is_connected = True
    async def disconnect(self): self.is_connected = False
    async def read_batch(self, limit=None):
        cnt = limit or self.config.batch_size
        records = [{"id": i, "user_id": f"u_{i}", "amount": float(i * 10)} for i in range(1, cnt + 1)]
        return RecordBatch(records=records, metadata={"source": "PostgreSQL"})

class PostgresSinkConnector(BaseSinkConnector):
    async def connect(self): self.is_connected = True
    async def disconnect(self): self.is_connected = False
    async def write_batch(self, batch: RecordBatch): return len(batch.records)
