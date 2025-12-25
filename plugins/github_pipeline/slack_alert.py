import json
import requests
from airflow.models import Variable


def notify_slack_failure(context):
    webhook = Variable.get("SLACK_WEBHOOK")

    dag_id = context["dag"].dag_id
    task_id = context["task_instance"].task_id
    log_url = context["task_instance"].log_url

    message = {
        "text": (
            "🚨 *Airflow Task Failed*\n"
            f"*DAG*: {dag_id}\n"
            f"*Task*: {task_id}\n"
            f"<{log_url}|View Logs>"
        )
    }

    requests.post(webhook, json=message, timeout=10)

def notify_slack_success(context):
    webhook = Variable.get("SLACK_WEBHOOK")

    dag_id = context["dag"].dag_id
    task_id = context["task_instance"].task_id

    message = {
        "text": (
            "✅ *Airflow Task Success*\n"
            f"*DAG*: {dag_id}\n"
            f"*Task*: {task_id}\n"
            "🎉 GitHub ingestion completed successfully"
        )
    }

    requests.post(webhook, json=message, timeout=10)
