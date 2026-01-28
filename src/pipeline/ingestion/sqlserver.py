import os
import pyodbc
from typing import Dict, List


def get_connection():
    return pyodbc.connect(
        driver="{ODBC Driver 17 for SQL Server}",
        server=os.getenv("SQLSERVER_HOST"),
        database=os.getenv("SQLSERVER_DB"),
        uid=os.getenv("SQLSERVER_USER"),
        pwd=os.getenv("SQLSERVER_PASSWORD"),
    )


def run_sqlserver_ingestion(source: Dict, run_date: str, bucket: str) -> List[Dict]:
    """
    Incremental ingestion from SQL Server.
    """

    table = source["table"]
    incremental_column = source.get("incremental_column", "updated_at")

    conn = get_connection()
    cursor = conn.cursor()

    query = f"""
        SELECT *
        FROM {table}
        WHERE {incremental_column} >= ?
    """

    cursor.execute(query, run_date)

    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    records = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()

    return records
