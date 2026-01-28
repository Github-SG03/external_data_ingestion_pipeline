import snowflake.connector
import json
from src.ingestion.writer import write_to_s3


def run_snowflake_etl(source, run_date, bucket):
    conn = snowflake.connector.connect(
        user=source["user"],
        password=source["password"],
        account=source["account"],
        warehouse=source["warehouse"],
        database=source["database"],
        schema=source["schema"],
    )

    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {source['table']} LIMIT 1000")
    rows = cur.fetchall()
    cols = [c[0] for c in cur.description]

    data = [dict(zip(cols, r)) for r in rows]
    key = f'{source["s3_prefix"]}/dt={run_date}/data.json'
    write_to_s3(bucket, key, json.dumps(data))

    cur.close()
    conn.close()
