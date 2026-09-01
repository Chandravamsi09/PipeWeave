"""Test Real DuckDB Vectorized Transformations"""
from pipeweave.transforms.duckdb_engine import DuckDBTransformEngine
from pipeweave.core.types import RecordBatch

def test_duckdb_vectorized_aggregation():
    sample_records = [
        {"customer_id": "CUST-01", "order_id": "ORD-1", "amount": 150.0, "status": "COMPLETED"},
        {"customer_id": "CUST-01", "order_id": "ORD-2", "amount": 250.0, "status": "COMPLETED"},
        {"customer_id": "CUST-02", "order_id": "ORD-3", "amount": 100.0, "status": "COMPLETED"},
        {"customer_id": "CUST-02", "order_id": "ORD-4", "amount": 50.0, "status": "PENDING"},
    ]
    batch = RecordBatch(records=sample_records)
    
    query = """
    SELECT 
        customer_id,
        COUNT(order_id) AS total_orders,
        SUM(amount) AS total_revenue,
        AVG(amount) AS avg_order_val
    FROM kafka_orders_stream
    WHERE status = 'COMPLETED'
    GROUP BY customer_id
    ORDER BY total_revenue DESC;
    """
    
    engine = DuckDBTransformEngine(query)
    result = engine.execute(batch)
    
    assert result.rows_in == 4
    assert result.rows_out == 2
    assert len(result.output_batch.records) == 2
    
    # Verify CUST-01 calculation
    cust1 = next(r for r in result.output_batch.records if r["customer_id"] == "CUST-01")
    assert cust1["total_orders"] == 2
    assert cust1["total_revenue"] == 400.0
    assert cust1["avg_order_val"] == 200.0
