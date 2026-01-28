from typing import Dict, List

from pipeline.metrics import record_success  # type: ignore
from pipeline.quality import run_quality_checks  # type: ignore
from pipeline.config import load_quality_rules  # type: ignore

from pipeline.ingestion.rest_api import run_rest_api_ingestion


def execute_source(source: Dict, run_date: str, bucket: str) -> List[Dict]:
    """
    STEP-2B executor:
    - Supports REST API ingestion
    - CI-safe
    - No writers yet
    """

    source_name = source["name"]
    source_type = source["type"]

    # ----------------------------
    # Dispatch (REST API only)
    # ----------------------------
    if source_type == "rest_api":
        records: List[Dict] = run_rest_api_ingestion(
            source=source,
            run_date=run_date,
            bucket=bucket,
        )
    else:
        # Other sources will be added incrementally
        records = []

    # ----------------------------
    # Data Quality
    # ----------------------------
    quality_rules = load_quality_rules().get(source_name, {})
    run_quality_checks(source_name, records, quality_rules)

    # ----------------------------
    # Metrics
    # ----------------------------
    record_success(source_name)

    return records
