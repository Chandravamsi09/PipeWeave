"""ClickHouse Sink"""
from .base import BaseSinkConnector

class ClickHouseSinkConnector(BaseSinkConnector):
    async def connect(self): self.is_connected = True
    async def disconnect(self): self.is_connected = False
    async def write_batch(self, batch): return len(batch.records)
