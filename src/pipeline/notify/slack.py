import os
import requests
from src.pipeline.logging import get_logger

logger = get_logger("SlackNotifier")

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")


def send_slack(message: str):
    if not SLACK_WEBHOOK:
        logger.warning("Slack webhook not configured")
        return

    payload = {"text": message}
    requests.post(SLACK_WEBHOOK, json=payload)


def notify_success(source: str, run_date: str):
    send_slack(f"✅ SUCCESS | Source: {source} | Date: {run_date}")


def notify_failure(source: str, run_date: str, error: str):
    send_slack(f"❌ FAILURE | Source: {source} | Date: {run_date}\nError: {error}")
