import os
import requests

JIRA_URL = os.getenv("JIRA_URL")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
JIRA_PROJECT = os.getenv("JIRA_PROJECT")


def create_incident(summary: str, description: str):
    if not all([JIRA_URL, JIRA_USER, JIRA_TOKEN]):
        return  # disabled in dev

    payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Incident"},
        }
    }

    requests.post(
        f"{JIRA_URL}/rest/api/2/issue",
        auth=(JIRA_USER, JIRA_TOKEN),  # type: ignore
        json=payload,
    )
