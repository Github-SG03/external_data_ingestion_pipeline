from typing import Dict, List

from pipeline.metrics import record_success  # type: ignore
from pipeline.quality import run_quality_checks  # type: ignore
from pipeline.config import load_quality_rules  # type: ignore

from pipeline.ingestion.rest_api import run_rest_api_ingestion
from pipeline.writer.s3_writer import write_json
from pipeline.ingestion.file import run_file_ingestion
from pipeline.ingestion.s3 import run_s3_ingestion


def execute_source(source: Dict, run_date: str, bucket: str) -> List[Dict]:
    source_name = source["name"]
    source_type = source["type"]

    if source_type == "rest_api":
        records: List[Dict] = run_rest_api_ingestion(
            source=source,
            run_date=run_date,
            bucket=bucket,
        )

        s3_key = f"{source['s3_prefix']}/dt={run_date}/data.json"
        write_json(bucket=bucket, key=s3_key, records=records)
    elif source_type == "file":
        records = run_file_ingestion(
            source=source,
            run_date=run_date,
            bucket=bucket,
        )
        s3_key = f"{source['s3_prefix']}/dt={run_date}/data.json"
        write_json(bucket=bucket, key=s3_key, records=records)

    elif source_type == "s3":
        records = run_s3_ingestion(
            source=source,
            run_date=run_date,
            bucket=bucket,
        )
        s3_key = f"{source['s3_prefix']}/dt={run_date}/data.json"
        write_json(bucket=bucket, key=s3_key, records=records)
    elif source_type == "sqlserver":
        from pipeline.ingestion.sqlserver import run_sqlserver_ingestion

        records = run_sqlserver_ingestion(
            source=source,
            run_date=run_date,
            bucket=bucket,
        )
        s3_key = f"{source['s3_prefix']}/dt={run_date}/data.json"
        write_json(bucket=bucket, key=s3_key, records=records)
    elif source_type == "snowflake":
        from pipeline.ingestion.snowflake import run_snowflake_ingestion

        records = run_snowflake_ingestion(
            source=source,
            run_date=run_date,
            bucket=bucket,
        )
        s3_key = f"{source['s3_prefix']}/dt={run_date}/data.json"
        write_json(bucket=bucket, key=s3_key, records=records)
    else:
        records = []

    quality_rules = load_quality_rules().get(source_name, {})
    run_quality_checks(source_name, records, quality_rules)

    record_success(source_name)
    return records
