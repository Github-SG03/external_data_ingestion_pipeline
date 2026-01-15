from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

from src.ingestion.config import load_sources, load_backfill
from src.ingestion.executor import run_ingestion
from src.ingestion.backfill import generate_dates

from github_pipeline.github_ingestion import run_github_etl
from github_pipeline.slack_alert.slack_alert import (
    notify_slack_failure,
    notify_slack_success,
)

DEFAULT_BUCKET = "your-s3-bucket"

def orchestrate():
    sources = load_sources()
    backfill = load_backfill()

    if backfill["enabled"]:
        dates = generate_dates(
            backfill["start_date"],
            backfill["end_date"]
        )
    else:
        from datetime import date
        dates = [date.today().strftime("%Y-%m-%d")]

    for run_date in dates:
        for source in sources:
            run_ingestion(
                source=source,
                run_date=run_date,
                bucket=DEFAULT_BUCKET
            )

default_args = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": notify_slack_failure,
    "on_success_callback": notify_slack_success,
}

with DAG(
    dag_id="external_data_ingestion",
    start_date=days_ago(1),
    schedule="@daily",
    catchup=False,
    tags=["phase2", "backfill", "config-driven"],
    max_active_runs=1,
    default_args=default_args,
) as dag:

     run_pipeline = PythonOperator(
        task_id="run_external_ingestion",
        python_callable=orchestrate
    )