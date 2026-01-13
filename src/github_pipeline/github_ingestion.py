import os
from datetime import datetime

import boto3
import pandas as pd
import requests
import yaml

from github_pipeline.metrics.metrics import PipelineMetrics


def load_config():
    env = os.getenv("ENV", "dev")
    config_path = f"{os.environ['AIRFLOW_HOME']}/config/{env}.yaml"

    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def run_github_etl(**kwargs):
    metrics = PipelineMetrics("github_ingestion")
    metrics.increment("runs_total")

    print("📥 Loading config...")
    config = load_config()

    sources = config["sources"]

    for source in sources:
        if not source["enabled"]:
            continue
        
        if source["type"] == "github":
            github_repo = source["repo"]
            # reuse same logic

    bucket = config["s3"]["bucket"]
    base_path = config["s3"]["base_path"]

    org = github_repo.split("/")[0]
    print(f"🔗 Fetching GitHub repos for org: {org}")

    url = f"https://api.github.com/orgs/{org}/repos"
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    repos = response.json()
    print(f"✅ Fetched {len(repos)} repositories")

    data = [
        {
            "repo": r["name"],
            "stars": r["stargazers_count"],
            "language": r["language"],
        }
        for r in repos
    ]

    df = pd.DataFrame(data)

    if df.empty:
        raise ValueError("DQ FAIL: No rows fetched")

    if "repo" not in df.columns:
        raise ValueError("DQ FAIL: Missing repo column")

    if df["stars"].isnull().any():
        raise ValueError("DQ FAIL: Null stars detected")

    date = datetime.utcnow().date().isoformat()
    output_path = f"{os.environ['AIRFLOW_HOME']}/logs/github_{date}.csv"

    df.to_csv(output_path, index=False)
    print(f"📄 File written to {output_path}")

    s3 = boto3.client("s3")
    s3_key = f"{base_path}/date={date}/github_{date}.csv"

    try:
        s3.upload_file(output_path, bucket, s3_key)
        print("⚠️ File already exists, skipping upload")

    except s3.exceptions.ClientError:
        s3.upload_file(output_path, bucket, s3_key)
        print("⬆️ Uploaded new file to S3")

    metrics.increment("success_total")
    print("🎉 GitHub ingestion completed successfully")
