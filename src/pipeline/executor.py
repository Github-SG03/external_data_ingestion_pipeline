import time

from src.pipeline.ingestion.github import run_github_ingestion  # type: ignore
from src.pipeline.ingestion.rest_api import run_rest_api_ingestion  # type: ignore
from src.pipeline.ingestion.file import run_file_ingestion  # type: ignore
from src.pipeline.ingestion.s3 import run_s3_ingestion  # type: ignore
from src.pipeline.ingestion.sqlserver import run_sqlserver_ingestion
from src.pipeline.ingestion.smtp import run_smtp_ingestion  # type: ignore
from src.pipeline.ingestion.snowflake import run_snowflake_ingestion  # type: ignore

from src.pipeline.quality import run_quality_checks  # type: ignore
from src.pipeline.config import load_quality_rules  # type: ignore


def execute_source(source: dict, run_date: str, bucket: str):
    source_type = source["type"]
    source_name = source["name"]

    # Dispatch to correct ingestion
    if source_type == "github":
        records = run_github_ingestion(source, run_date, bucket)

    elif source_type == "rest_api":
        records = run_rest_api_ingestion(source, run_date, bucket)

    elif source_type == "file":
        records = run_file_ingestion(source, run_date, bucket)

    elif source_type == "s3":
        records = run_s3_ingestion(source, run_date, bucket)

    elif source_type == "sqlserver":
        records = run_sqlserver_ingestion(source, run_date, bucket)

    elif source_type == "smtp" and source.get("enabled", False):
        records = run_smtp_ingestion(source, run_date, bucket)

    elif source_type == "snowflake" and source.get("enabled", False):
        records = run_snowflake_ingestion(source, run_date, bucket)

    elif source_type == "sqlserver":
        records = run_sqlserver_ingestion(source, run_date, bucket)

    else:
        raise ValueError(f"Unsupported or disabled source: {source_name}")

    # Run Data Quality
    quality_rules = load_quality_rules().get(source_name, {})
    run_quality_checks(source_name, records, quality_rules)

    # observable.
    start = time.time()  # type: ignore
    records = run_source(...)  # type: ignore
    duration = time.time() - start  # type: ignore
    record_success(source_name, len(records), duration)  # type: ignore

    return records
