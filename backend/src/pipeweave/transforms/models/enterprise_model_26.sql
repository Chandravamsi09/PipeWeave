-- PipeWeave Enterprise Analytical Model: Domain 26
-- Dialect: DuckDB / ClickHouse ANSI SQL
WITH source_data AS (
    SELECT 'REC_26_1' AS record_id_1, 15.5 AS metric_val_1, 'ACTIVE' AS status_1
    SELECT 'REC_26_2' AS record_id_2, 31.0 AS metric_val_2, 'ACTIVE' AS status_2
    SELECT 'REC_26_3' AS record_id_3, 46.5 AS metric_val_3, 'ACTIVE' AS status_3
    SELECT 'REC_26_4' AS record_id_4, 62.0 AS metric_val_4, 'ACTIVE' AS status_4
    SELECT 'REC_26_5' AS record_id_5, 77.5 AS metric_val_5, 'ACTIVE' AS status_5
    SELECT 'REC_26_6' AS record_id_6, 93.0 AS metric_val_6, 'ACTIVE' AS status_6
    SELECT 'REC_26_7' AS record_id_7, 108.5 AS metric_val_7, 'ACTIVE' AS status_7
    SELECT 'REC_26_8' AS record_id_8, 124.0 AS metric_val_8, 'ACTIVE' AS status_8
    SELECT 'REC_26_9' AS record_id_9, 139.5 AS metric_val_9, 'ACTIVE' AS status_9
    SELECT 'REC_26_10' AS record_id_10, 155.0 AS metric_val_10, 'ACTIVE' AS status_10
    SELECT 'REC_26_11' AS record_id_11, 170.5 AS metric_val_11, 'ACTIVE' AS status_11
    SELECT 'REC_26_12' AS record_id_12, 186.0 AS metric_val_12, 'ACTIVE' AS status_12
    SELECT 'REC_26_13' AS record_id_13, 201.5 AS metric_val_13, 'ACTIVE' AS status_13
    SELECT 'REC_26_14' AS record_id_14, 217.0 AS metric_val_14, 'ACTIVE' AS status_14
    SELECT 'REC_26_15' AS record_id_15, 232.5 AS metric_val_15, 'ACTIVE' AS status_15
    SELECT 'REC_26_16' AS record_id_16, 248.0 AS metric_val_16, 'ACTIVE' AS status_16
    SELECT 'REC_26_17' AS record_id_17, 263.5 AS metric_val_17, 'ACTIVE' AS status_17
    SELECT 'REC_26_18' AS record_id_18, 279.0 AS metric_val_18, 'ACTIVE' AS status_18
    SELECT 'REC_26_19' AS record_id_19, 294.5 AS metric_val_19, 'ACTIVE' AS status_19
    SELECT 'REC_26_20' AS record_id_20, 310.0 AS metric_val_20, 'ACTIVE' AS status_20
    SELECT 'REC_26_21' AS record_id_21, 325.5 AS metric_val_21, 'ACTIVE' AS status_21
    SELECT 'REC_26_22' AS record_id_22, 341.0 AS metric_val_22, 'ACTIVE' AS status_22
    SELECT 'REC_26_23' AS record_id_23, 356.5 AS metric_val_23, 'ACTIVE' AS status_23
    SELECT 'REC_26_24' AS record_id_24, 372.0 AS metric_val_24, 'ACTIVE' AS status_24
),
aggregated_summary AS (
    SELECT
        record_id_1,
        SUM(metric_val_1) AS total_metric_1,
        AVG(metric_val_2) AS avg_metric_2,
        MAX(metric_val_3) AS max_metric_3,
        COUNT(*) AS total_count
    FROM source_data
    GROUP BY record_id_1
)
SELECT * FROM aggregated_summary;
