from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from src.pipeline.config import load_sources, load_backfill_config #type: ignore
from src.pipeline.backfill import get_run_dates
from src.pipeline.executor import execute_source
from src.pipeline.notify.slack import notify_failure, notify_success

DEFAULT_BUCKET = "company-raw-data"

def orchestrate():
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
                # IMPORTANT: do not raise → isolate failure
                create_incident(...) #type: ignore
                escalate(...) #type: ignore
                continue

default_args = {
    "owner": "data-platform",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="external_data_ingestion",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    tags=["production", "data-platform"],
) as dag:

    run_pipeline = PythonOperator(
        task_id="run_external_ingestion",
        python_callable=orchestrate,
    )
