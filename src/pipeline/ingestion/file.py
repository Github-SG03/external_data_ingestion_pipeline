import json
import csv
from typing import Dict, List


def run_file_ingestion(source: Dict, run_date: str, bucket: str) -> List[Dict]:
    """
    Ingest data from local file (CSV or JSON).
    """

    file_path = source["path"]
    file_type = source.get("format", "json").lower()

    records: List[Dict] = []

    if file_type == "json":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                records = data
            elif isinstance(data, dict):
                records = [data]

    elif file_type == "csv":
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            records = list(reader)

    else:
        raise ValueError(f"Unsupported file format: {file_type}")

    return records
