from typing import Dict, List


def run_snowflake_ingestion(source: Dict, run_date: str, bucket: str) -> List[Dict]:
    """
    Read data from Snowflake (read-only).
    Lazy import to keep CI safe.
    """

    import snowflake.connector

    conn = snowflake.connector.connect(
        user=source["user"],
        password=source["password"],
        account=source["account"],
        warehouse=source["warehouse"],
        database=source["database"],
        schema=source["schema"],
    )

    cursor = conn.cursor()

    query = source["query"]
    cursor.execute(query)

    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    records = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()

    return records
