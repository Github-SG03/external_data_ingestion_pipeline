import json
import boto3
from pipeline.logging import get_logger

logger = get_logger("S3Writer")
s3 = boto3.client("s3")


def write_json(bucket: str, key: str, records):
    """
    Write list of dicts as JSON to S3.
    """
    body = json.dumps(records)
    logger.info(f"Writing {len(records)} records to s3://{bucket}/{key}")
    s3.put_object(Bucket=bucket, Key=key, Body=body)
