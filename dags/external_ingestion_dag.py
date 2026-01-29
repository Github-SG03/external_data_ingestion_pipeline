from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from pipeline.executor import orchestrate

default_args = {
    "owner": "data-platform",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="external_data_ingestion",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    default_args=default_args,
    tags=["production", "data-platform"],
) as dag:

    run_external_ingestion = PythonOperator(
        task_id="run_external_ingestion",
        python_callable=orchestrate,
    )
