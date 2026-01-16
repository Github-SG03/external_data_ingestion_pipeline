import os
import json
import pyodbc
from src.pipeline.writer.s3_writer import write_json
from src.pipeline.logging import get_logger

logger = get_logger("SQLServerIngestion")

def get_sqlserver_connection():
    return pyodbc.connect(
        driver="{ODBC Driver 17 for SQL Server}",
        server=os.getenv("SQLSERVER_HOST"),
        database=os.getenv("SQLSERVER_DB"),
        uid=os.getenv("SQLSERVER_USER"),
        pwd=os.getenv("SQLSERVER_PASSWORD"),
    )

def run_sqlserver_ingestion(source: dict, run_date: str, bucket: str):
    """
    Read-only incremental ingestion from SQL Server.
    """
    table = source["table"]
    incr_col = source.get("incremental_column", "updated_at")

    logger.info(f"Starting SQL Server ingestion for {table}")

    conn = get_sqlserver_connection()
    cursor = conn.cursor()

    query = f"""
        SELECT *
        FROM {table}
        WHERE {incr_col} >= ?
    """
    cursor.execute(query, run_date)

    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    records = [dict(zip(columns, row)) for row in rows]

    key = f"{source['s3_prefix']}/dt={run_date}/data.json"
    write_json(bucket, key, json.dumps(records))

    logger.info(
        f"Completed SQL Server ingestion for {table} | Rows: {len(records)}"
    )

    cursor.close()
    conn.close()

    return records
