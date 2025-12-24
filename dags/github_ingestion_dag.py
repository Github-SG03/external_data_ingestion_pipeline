from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta
from github_pipeline.github_ingestion import run_github_etl
from github_pipeline.slack_alert import notify_slack

default_args = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": notify_slack,
    "on_success_callback": notify_slack,
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

