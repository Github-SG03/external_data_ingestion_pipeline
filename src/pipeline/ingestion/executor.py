from github_pipeline.metrics.metrics import record_success, record_failure #type: ignore
from src.ingestion.github import run_github_etl  #type: ignore
from github_pipeline.metrics.metrics import record_success, record_failure #type: ignore
from github_pipeline.metrics.metrics import record_success, record_failure #type: ignore
from src.ingestion.rest_api import run_rest_api_etl  #type: ignore
from github_pipeline.metrics.metrics import record_success, record_failure #type: ignore
from github_pipeline.metrics.metrics import record_success, record_failure #type: ignore
from github_pipeline.metrics.metrics import record_success, record_failure #type: ignore
from src.ingestion.file import run_file_etl   #type: ignore
from src.ingestion.s3 import run_s3_etl   #type: ignore
from src.ingestion.smtp import run_smtp_etl #type: ignore
from src.ingestion.snowflake import run_snowflake_etl #type: ignore

from github_pipeline.metrics.metrics import record_success, record_failure #type: ignore
from github_pipeline.slack_alert.slack_alert import (   #type: ignore
    notify_slack_success,
    notify_slack_failure,
)   

def run_ingestion(source, run_date, bucket):
    try:
        source_type = source["type"]

        if source_type == "github":
            run_github_etl(source, run_date, bucket)

        elif source_type == "rest_api":
            run_rest_api_etl(source, run_date, bucket)

        elif source_type == "file":
            run_file_etl(source, run_date, bucket)

        elif source_type == "s3":
            run_s3_etl(source, run_date, bucket)

        elif source_type == "smtp":
            # SAFE: skip if not configured
            if source.get("enabled", False):
                run_smtp_etl(source, run_date, bucket)

        elif source_type == "snowflake":
            # SAFE: read-only
            if source.get("enabled", False):
                run_snowflake_etl(source, run_date, bucket)

        else:
            raise ValueError(f"Unsupported source type: {source_type}")

        record_success(source["name"])
        notify_slack_success(None)

    except Exception as e:
        record_failure(source["name"])
        notify_slack_failure(None)
        raise
