import requests
from typing import Dict, List


def run_rest_api_ingestion(source: Dict, run_date: str, bucket: str) -> List[Dict]:
    """
    Fetch data from a REST API source.
    This is STEP-2 ingestion logic.
    """

    url = source["url"]
    params = source.get("params", {})

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    # Normalize to list of records
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return data

    return []
