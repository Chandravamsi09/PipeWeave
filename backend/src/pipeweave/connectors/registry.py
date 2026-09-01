"""Connector Registry"""
from .postgres import PostgresSourceConnector, PostgresSinkConnector
from .kafka import KafkaSourceConnector, KafkaSinkConnector
from .s3_parquet import S3ParquetSourceConnector, S3ParquetSinkConnector
from .clickhouse import ClickHouseSinkConnector
from ..core.constants import ConnectorType

class ConnectorRegistry:
    def __init__(self):
        self.sources = {ConnectorType.POSTGRESQL.value: PostgresSourceConnector, ConnectorType.KAFKA.value: KafkaSourceConnector, ConnectorType.S3_PARQUET.value: S3ParquetSourceConnector}
        self.sinks = {ConnectorType.POSTGRESQL.value: PostgresSinkConnector, ConnectorType.KAFKA.value: KafkaSinkConnector, ConnectorType.CLICKHOUSE.value: ClickHouseSinkConnector}
    def list_available_connectors(self): return {"sources": list(self.sources.keys()), "sinks": list(self.sinks.keys())}

connector_registry = ConnectorRegistry()
