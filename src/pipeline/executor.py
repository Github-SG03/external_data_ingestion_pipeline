from typing import Dict, List


def execute_source(source: Dict, run_date: str, bucket: str) -> List[Dict]:
    """
    Executes ingestion for a single source & date.
    SAFE for Airflow import.
    """

    # ✅ local imports ONLY (Airflow-safe)
    from pipeline.metrics import record_success
    from pipeline.quality import run_quality_checks
    from pipeline.config import load_quality_rules
    from pipeline.writer.s3_writer import write_json

    source_name = source["name"]
    source_type = source["type"]

    records: List[Dict] = []

    if source_type == "rest_api":
        from pipeline.ingestion.rest_api import run_rest_api_ingestion

        records = run_rest_api_ingestion(source, run_date, bucket)

    elif source_type == "file":
        from pipeline.ingestion.file import run_file_ingestion

        records = run_file_ingestion(source, run_date, bucket)

    elif source_type == "s3":
        from pipeline.ingestion.s3 import run_s3_ingestion

        records = run_s3_ingestion(source, run_date, bucket)

    elif source_type == "sqlserver":
        from pipeline.ingestion.sqlserver import run_sqlserver_ingestion

        records = run_sqlserver_ingestion(source, run_date, bucket)

    elif source_type == "snowflake":
        from pipeline.ingestion.snowflake import run_snowflake_ingestion

        records = run_snowflake_ingestion(source, run_date, bucket)

    elif source_type == "smtp":
        from pipeline.ingestion.smtp import run_smtp_ingestion

        records = run_smtp_ingestion(source, run_date, bucket)

    # Write to S3 (common)
    if records:
        s3_key = f"{source['s3_prefix']}/dt={run_date}/data.json"
        write_json(bucket=bucket, key=s3_key, records=records)

    # Data Quality
    quality_rules = load_quality_rules().get(source_name, {})
    run_quality_checks(source_name, records, quality_rules)

    record_success(source_name)
    return records


def orchestrate():
    """
    MAIN ORCHESTRATION ENTRYPOINT
    This is what Airflow calls.
    """

    # ✅ ALL imports moved inside
    from pipeline.config import load_sources, load_backfill_config
    from pipeline.backfill import get_run_dates
    from pipeline.notify.slack import notify_failure, notify_success

    DEFAULT_BUCKET = "company-raw-data"

    sources = load_sources()
    backfill_cfg = load_backfill_config()
    run_dates = get_run_dates(backfill_cfg)

    for run_date in run_dates:
        for source in sources:
            source_name = source["name"]
            try:
                execute_source(
                    source=source,
                    run_date=run_date,
                    bucket=DEFAULT_BUCKET,
                )
                notify_success(source_name, run_date)

            except Exception as e:
                notify_failure(source_name, run_date, str(e))
                # isolate failure — DO NOT crash DAG
                continue
