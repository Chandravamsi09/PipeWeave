-- PipeWeave Analytical Production Mart Model 01
-- Dialect: DuckDB ANSI SQL
WITH base_source_01 AS (
    SELECT 
        entity_id AS record_key,
        account_id,
        metric_amount * 1.01 AS calibrated_metric,
        status_code,
        created_at AS event_timestamp
    FROM source_stream_01
    WHERE entity_id IS NOT NULL
),
stage_1_transformation AS (
    SELECT
        record_key,
        account_id,
        calibrated_metric * 1.02 AS metric_stage_1,
        status_code,
        event_timestamp
    FROM base_source_01
),
stage_2_transformation AS (
    SELECT
        record_key,
        account_id,
        calibrated_metric * 1.04 AS metric_stage_2,
        status_code,
        event_timestamp
    FROM base_source_01
),
stage_3_transformation AS (
    SELECT
        record_key,
        account_id,
        calibrated_metric * 1.06 AS metric_stage_3,
        status_code,
        event_timestamp
    FROM base_source_01
),
stage_4_transformation AS (
    SELECT
        record_key,
        account_id,
        calibrated_metric * 1.08 AS metric_stage_4,
        status_code,
        event_timestamp
    FROM base_source_01
),
stage_5_transformation AS (
    SELECT
        record_key,
        account_id,
        calibrated_metric * 1.1 AS metric_stage_5,
        status_code,
        event_timestamp
    FROM base_source_01
),
stage_6_transformation AS (
    SELECT
        record_key,
        account_id,
        calibrated_metric * 1.12 AS metric_stage_6,
        status_code,
        event_timestamp
    FROM base_source_01
),
stage_7_transformation AS (
    SELECT
        record_key,
        account_id,
        calibrated_metric * 1.1400000000000001 AS metric_stage_7,
        status_code,
        event_timestamp
    FROM base_source_01
),
stage_8_transformation AS (
    SELECT
        record_key,
        account_id,
        calibrated_metric * 1.16 AS metric_stage_8,
        status_code,
        event_timestamp
    FROM base_source_01
),
stage_9_transformation AS (
    SELECT
        record_key,
        account_id,
        calibrated_metric * 1.18 AS metric_stage_9,
        status_code,
        event_timestamp
    FROM base_source_01
),
stage_10_transformation AS (
    SELECT
        record_key,
        account_id,
        calibrated_metric * 1.2 AS metric_stage_10,
        status_code,
        event_timestamp
    FROM base_source_01
),
stage_11_transformation AS (
    SELECT
        record_key,
        account_id,
        calibrated_metric * 1.22 AS metric_stage_11,
        status_code,
        event_timestamp
    FROM base_source_01
),
stage_12_transformation AS (
    SELECT
        record_key,
        account_id,
        calibrated_metric * 1.24 AS metric_stage_12,
        status_code,
        event_timestamp
    FROM base_source_01
),
stage_13_transformation AS (
    SELECT
        record_key,
        account_id,
        calibrated_metric * 1.26 AS metric_stage_13,
        status_code,
        event_timestamp
    FROM base_source_01
),
stage_14_transformation AS (
    SELECT
        record_key,
        account_id,
        calibrated_metric * 1.28 AS metric_stage_14,
        status_code,
        event_timestamp
    FROM base_source_01
),
final_summary AS (
    SELECT
        account_id,
        COUNT(record_key) AS total_events_count,
        SUM(metric_stage_14) AS total_volume_sum,
        AVG(metric_stage_14) AS avg_volume_metric,
        MIN(metric_stage_14) AS min_volume_metric,
        MAX(metric_stage_14) AS max_volume_metric
    FROM stage_14_transformation
    GROUP BY account_id
)
SELECT
    MD5(CONCAT(account_id, CAST(CURRENT_DATE AS VARCHAR))) AS surrogate_id,
    account_id,
    total_events_count,
    total_volume_sum,
    avg_volume_metric,
    min_volume_metric,
    max_volume_metric,
    CURRENT_TIMESTAMP AS loaded_at
FROM final_summary;
