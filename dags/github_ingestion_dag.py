from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from plugins.github_pipeline.github_ingestion import run_github_etl
from plugins.github_pipeline.slack_alert.slack_alert import (
    notify_slack_failure,
    notify_slack_success,
)

default_args = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": notify_slack_failure,
    "on_success_callback": notify_slack_success,
}

with DAG(
    dag_id="github_ingestion",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
) as dag:
    github_task = PythonOperator(
        task_id="github_etl",
        python_callable=run_github_etl,
    )
