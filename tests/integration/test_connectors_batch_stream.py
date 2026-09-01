"""Integration Tests for Connectors"""
import asyncio
from pipeweave.connectors.postgres import PostgresSourceConnector, PostgresSinkConnector
from pipeweave.connectors.kafka import KafkaSourceConnector, KafkaSinkConnector
from pipeweave.connectors.base import ConnectorConfig

def test_postgres_connector():
    async def _test():
        cfg = ConnectorConfig(connector_type="POSTGRESQL", batch_size=20)
        src = PostgresSourceConnector(cfg); sink = PostgresSinkConnector(cfg)
        await src.connect(); await sink.connect()
        batch = await src.read_batch(limit=10)
        assert batch.row_count == 10
        assert await sink.write_batch(batch) == 10
        await src.disconnect()
    asyncio.run(_test())

def test_kafka_connector():
    async def _test():
        cfg = ConnectorConfig(connector_type="KAFKA", topic="test_topic")
        src = KafkaSourceConnector(cfg); sink = KafkaSinkConnector(cfg)
        await src.connect()
        batch = await src.read_batch(limit=50)
        assert batch.row_count == 50
        assert await sink.write_batch(batch) == 50
        await src.disconnect()
    asyncio.run(_test())
