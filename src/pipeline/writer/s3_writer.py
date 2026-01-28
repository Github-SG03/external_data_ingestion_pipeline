import boto3
from src.pipeline.logging import get_logger

logger = get_logger("S3Writer")
s3 = boto3.client("s3")


def write_json(bucket: str, key: str, data: str):
    logger.info(f"Writing to s3://{bucket}/{key}")
    s3.put_object(Bucket=bucket, Key=key, Body=data)
