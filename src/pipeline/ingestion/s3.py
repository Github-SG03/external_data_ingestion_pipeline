import boto3
from src.github_pipeline.github_ingestion import run_github_etl  # type: ignore

s3 = boto3.client("s3")


def run_s3_etl(source, run_date, bucket):
    objects = s3.list_objects_v2(
        Bucket=source["source_bucket"], Prefix=source.get("prefix", "")
    ).get("Contents", [])

    for obj in objects:
        data = s3.get_object(Bucket=source["source_bucket"], Key=obj["Key"])[
            "Body"
        ].read()

        key = f'{source["s3_prefix"]}/dt={run_date}/{obj["Key"].split("/")[-1]}'
        write_to_s3(bucket, key, data)  # type: ignore
