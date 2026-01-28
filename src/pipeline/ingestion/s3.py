import json
import boto3
from typing import Dict, List

s3 = boto3.client("s3")


def run_s3_ingestion(source: Dict, run_date: str, bucket: str) -> List[Dict]:
    """
    Ingest data from a source S3 bucket and return records.
    """

    source_bucket = source["source_bucket"]
    prefix = source.get("prefix", "")

    response = s3.list_objects_v2(
        Bucket=source_bucket,
        Prefix=prefix,
    )

    records: List[Dict] = []

    for obj in response.get("Contents", []):
        key = obj["Key"]

        body = s3.get_object(
            Bucket=source_bucket,
            Key=key,
        )["Body"].read()

        data = json.loads(body)

        if isinstance(data, list):
            records.extend(data)
        elif isinstance(data, dict):
            records.append(data)

    return records
