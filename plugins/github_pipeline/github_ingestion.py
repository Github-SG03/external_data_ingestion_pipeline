import os
import requests
import pandas as pd
import yaml
from datetime import datetime
import boto3
from github_pipeline.metrics import PipelineMetrics


def load_config():
    env = os.getenv("ENV", "dev")
    config_path = f"{os.environ['AIRFLOW_HOME']}/config/{env}.yaml"

    with open(config_path) as f:
        return yaml.safe_load(f)


def run_github_etl(**context):
    metrics = PipelineMetrics("github_ingestion")
    metrics.increment("runs_total")

    print("📥 Loading config...")
    config = load_config()

    # ---- CONFIG VALUES ----
    github_repo = config["github"]["repo"]   # e.g. apache/airflow
    bucket = config["s3"]["bucket"]
    base_path = config["s3"]["base_path"]
    org = github_repo.split("/")[0]

    print(f"🔗 Fetching GitHub repos for org: {org}")
         url = f"https://api.github.com/orgs/{org}/repos"
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    repos = response.json()
    print(f"✅ Fetched {len(repos)} repositories")

    # ---- TRANSFORM ----
    data = [
        {
            "repo": r["name"],
            "stars": r["stargazers_count"],
            "language": r["language"]
        }
        for r in repos
    ]

    df = pd.DataFrame(data)

    if df.empty:
        raise ValueError("❌ No data fetched from GitHub API")
      
    # ---- SAVE LOCALLY (Airflow logs) ----
    date = context.get("ds")
    output_path = f"{os.environ['AIRFLOW_HOME']}/logs/github_{date}.csv"

    df.to_csv(output_path, index=False)
    print(f"📄 File written to {output_path}")

        # Upload to S3
    s3 = boto3.client("s3")
    s3_key = f"{base_path}/date={date}/github_{date}.csv"
    s3.upload_file(output_path, bucket, s3_key)

    metrics.increment("success_total")
    print("🎉 GitHub ingestion completed successfully")
