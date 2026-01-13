from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from github_pipeline.github_ingestion import run_github_etl
from github_pipeline.github_ingestion import run_github_etl
from github_pipeline.slack_alert.slack_alert import (
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
    catchup=True,
    max_active_runs=1,
    default_args=default_args,
) as dag:

    #Task 1:Fetch github data from github API
    task_extract_data = PythonOperator(
        task_id="extract_data",
        python_callable=run_github_etl,
    )
    
    #Task 2:Transform github  fetched API data
     task_transform_data = PythonOperator(
        task_id="transform_data",
        python_callable=run_github_etl,
    )


    #Task 3:Load github fetched API data
     task_load_data = PythonOperator(
        task_id="load_data",
        python_callable=run_github_etl,
    )

task_extract_data >> task_transform_data >> task_load_data
