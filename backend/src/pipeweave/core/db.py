"""
PipeWeave SQLite Persistence & Repository Layer
"""
import sqlite3
import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

# Compute root project directory
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "pipeweave.db"))

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_tables():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS pipelines (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            schedule TEXT,
            status TEXT DEFAULT 'ACTIVE',
            dag_definition TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS pipeline_runs (
            run_id TEXT PRIMARY KEY,
            pipeline_id TEXT NOT NULL,
            state TEXT NOT NULL,
            records_processed INTEGER DEFAULT 0,
            duration_ms REAL DEFAULT 0.0,
            node_outputs TEXT,
            error_message TEXT,
            started_at TEXT NOT NULL,
            finished_at TEXT,
            FOREIGN KEY (pipeline_id) REFERENCES pipelines (id)
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS schema_registry (
            subject TEXT NOT NULL,
            version INTEGER NOT NULL,
            schema_type TEXT NOT NULL,
            schema_definition TEXT NOT NULL,
            compatibility_mode TEXT DEFAULT 'BACKWARD',
            created_at TEXT NOT NULL,
            PRIMARY KEY (subject, version)
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS connectors (
            name TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            host TEXT NOT NULL,
            status TEXT DEFAULT 'ONLINE',
            config TEXT,
            created_at TEXT NOT NULL
        )
        """)
        
        # Seed default pipeline if not present
        cur.execute("SELECT COUNT(*) FROM pipelines WHERE id = 'pipe-ecom'")
        if cur.fetchone()[0] == 0:
            default_dag = {
                "id": "pipe-ecom",
                "name": "E-Commerce Real-Time Order Stream",
                "description": "High-throughput real-time order ingestion, validation, and analytics",
                "nodes": [
                    {"id": "source_kafka", "name": "Kafka Orders Stream", "type": "SOURCE", "desc": "Real-time JSON/Avro events topic"},
                    {"id": "clean_nulls", "name": "Null Sanitizer & Imputer", "type": "TRANSFORM", "desc": "Cleanse & normalize payload fields"},
                    {"id": "quality_gate", "name": "Great Expectations Gate", "type": "QUALITY_GATE", "desc": "Rule check: amount > 0, valid email"},
                    {"id": "revenue_agg", "name": "Tumbling Revenue Window", "type": "TRANSFORM", "desc": "Vectorized 60s sliding window aggregate"},
                    {"id": "sink_clickhouse", "name": "ClickHouse Columnar Mart", "type": "SINK", "desc": "Fast columnar analytics warehouse"}
                ],
                "edges": [
                    {"source": "source_kafka", "target": "clean_nulls"},
                    {"source": "clean_nulls", "target": "quality_gate"},
                    {"source": "quality_gate", "target": "revenue_agg"},
                    {"source": "revenue_agg", "target": "sink_clickhouse"}
                ]
            }
            now = datetime.now(timezone.utc).isoformat()
            cur.execute(
                "INSERT OR REPLACE INTO pipelines (id, name, description, dag_definition, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                ("pipe-ecom", "E-Commerce Real-Time Order Stream", default_dag["description"], json.dumps(default_dag), now, now)
            )
            
            connectors_seed = [
                ("Production Kafka Broker", "KAFKA", "kafka.prod.internal:9092", "ONLINE", json.dumps({"topic": "orders.v1"})),
                ("PostgreSQL Read Replica", "POSTGRESQL", "pg-replica.internal:5432", "ONLINE", json.dumps({"database": "orders_db"})),
                ("ClickHouse Columnar Sink", "CLICKHOUSE", "clickhouse.cluster:8123", "ONLINE", json.dumps({"table": "fct_orders_mart"})),
                ("S3 Parquet Data Lake", "S3_PARQUET", "s3://production-lakehouse/", "ONLINE", json.dumps({"bucket": "production-lakehouse"}))
            ]
            for name, c_type, host, status, cfg in connectors_seed:
                cur.execute("INSERT OR REPLACE INTO connectors VALUES (?, ?, ?, ?, ?, ?)", (name, c_type, host, status, cfg, now))

            s_v1 = {"type": "record", "name": "OrderEvent", "fields": [{"name": "order_id", "type": "string"}, {"name": "customer_id", "type": "string"}, {"name": "amount", "type": "double"}]}
            s_v2 = {"type": "record", "name": "OrderEvent", "fields": [{"name": "order_id", "type": "string"}, {"name": "customer_id", "type": "string"}, {"name": "amount", "type": "double"}, {"name": "currency", "type": "string", "default": "USD"}, {"name": "status", "type": "string", "default": "PENDING"}]}
            cur.execute("INSERT OR REPLACE INTO schema_registry VALUES (?, ?, ?, ?, ?, ?)", ("orders-value", 1, "AVRO", json.dumps(s_v1), "BACKWARD", now))
            cur.execute("INSERT OR REPLACE INTO schema_registry VALUES (?, ?, ?, ?, ?, ?)", ("orders-value", 2, "AVRO", json.dumps(s_v2), "BACKWARD", now))

        conn.commit()

init_tables()

class PipelineRepository:
    @staticmethod
    def list_all() -> List[Dict[str, Any]]:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM pipelines ORDER BY created_at DESC")
            rows = cur.fetchall()
            results = []
            for r in rows:
                item = dict(r)
                item["dag_definition"] = json.loads(item["dag_definition"])
                item["nodes_count"] = len(item["dag_definition"].get("nodes", []))
                results.append(item)
            return results

    @staticmethod
    def get_by_id(pipeline_id: str) -> Optional[Dict[str, Any]]:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM pipelines WHERE id = ?", (pipeline_id,))
            row = cur.fetchone()
            if not row:
                return None
            item = dict(row)
            item["dag_definition"] = json.loads(item["dag_definition"])
            return item

    @staticmethod
    def save(pipeline: Dict[str, Any]):
        with get_db() as conn:
            cur = conn.cursor()
            now = datetime.now(timezone.utc).isoformat()
            dag_str = json.dumps(pipeline.get("dag_definition", {}))
            cur.execute(
                """
                INSERT INTO pipelines (id, name, description, schedule, status, dag_definition, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name=excluded.name,
                    description=excluded.description,
                    dag_definition=excluded.dag_definition,
                    updated_at=excluded.updated_at
                """,
                (pipeline["id"], pipeline["name"], pipeline.get("description", ""), pipeline.get("schedule", ""), pipeline.get("status", "ACTIVE"), dag_str, now, now)
            )
            conn.commit()

class RunRepository:
    @staticmethod
    def list_all(limit: int = 50) -> List[Dict[str, Any]]:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT r.*, p.name as pipeline_name FROM pipeline_runs r LEFT JOIN pipelines p ON r.pipeline_id = p.id ORDER BY r.started_at DESC LIMIT ?", (limit,))
            rows = cur.fetchall()
            results = []
            for r in rows:
                item = dict(r)
                if item.get("node_outputs"):
                    try:
                        item["node_outputs"] = json.loads(item["node_outputs"])
                    except Exception:
                        pass
                results.append(item)
            return results

    @staticmethod
    def save(run_data: Dict[str, Any]):
        with get_db() as conn:
            cur = conn.cursor()
            node_out_str = json.dumps(run_data.get("node_outputs", {}))
            cur.execute(
                """
                INSERT OR REPLACE INTO pipeline_runs (run_id, pipeline_id, state, records_processed, duration_ms, node_outputs, error_message, started_at, finished_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (run_data["run_id"], run_data["pipeline_id"], run_data["state"], run_data.get("records_processed", 0), run_data.get("duration_ms", 0.0), node_out_str, run_data.get("error_message"), run_data["started_at"], run_data.get("finished_at"))
            )
            conn.commit()

class SchemaRepository:
    @staticmethod
    def list_all() -> List[Dict[str, Any]]:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM schema_registry ORDER BY subject ASC, version DESC")
            rows = cur.fetchall()
            results = []
            for r in rows:
                item = dict(r)
                item["schema_definition"] = json.loads(item["schema_definition"])
                results.append(item)
            return results

    @staticmethod
    def save(subject: str, version: int, schema_type: str, schema_def: Dict[str, Any], compatibility: str = "BACKWARD"):
        with get_db() as conn:
            cur = conn.cursor()
            now = datetime.now(timezone.utc).isoformat()
            cur.execute(
                """
                INSERT OR REPLACE INTO schema_registry (subject, version, schema_type, schema_definition, compatibility_mode, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (subject, version, schema_type, json.dumps(schema_def), compatibility, now)
            )
            conn.commit()

class ConnectorRepository:
    @staticmethod
    def list_all() -> List[Dict[str, Any]]:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM connectors ORDER BY name ASC")
            rows = cur.fetchall()
            results = []
            for r in rows:
                item = dict(r)
                if item.get("config"):
                    try:
                        item["config"] = json.loads(item["config"])
                    except Exception:
                        pass
                results.append(item)
            return results
