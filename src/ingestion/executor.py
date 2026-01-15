from src.ingestion.loader import fetch_github_repo
from src.ingestion.writer import write_to_s3
from src.github_pipeline.metrics.metrics import record_success, record_failure
from src.github_pipeline.slack_alert.slack_alert import send_slack_alert
import json

def run_ingestion(source: dict, run_date: str, bucket: str):
    try:
        data = fetch_github_repo(
            owner=source["owner"],
            repo=source["repo"]
        )

        key = f'{source["s3_prefix"]}/dt={run_date}/data.json'

        write_to_s3(
            bucket=bucket,
            key=key,
            body=json.dumps(data)
        )

        record_success(source["name"])
        send_slack_alert(f"✅ Ingestion success: {source['name']} ({run_date})")

    except Exception as e:
        record_failure(source["name"])
        send_slack_alert(f"❌ Ingestion failed: {source['name']} ({run_date})\n{e}")
        raise
