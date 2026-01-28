import time
from typing import Dict, List

from pipeline.metrics import record_success  # type: ignore
from pipeline.quality import run_quality_checks  # type: ignore
from pipeline.config import load_quality_rules  # type: ignore


def execute_source(source: Dict, run_date: str, bucket: str) -> List[Dict]:
    """
    Phase-1 executor:
    - Dispatch-safe
    - No real ingestion
    - CI / DAG import friendly
    """

    source_name = source["name"]

    # ------------------------------------------------------------------
    # PLACEHOLDER: real ingestion will be wired in STEP-2
    # ------------------------------------------------------------------
    records: List[Dict] = []

    # ------------------------------------------------------------------
    # Data Quality (safe even with empty records)
    # ------------------------------------------------------------------
    quality_rules = load_quality_rules().get(source_name, {})
    run_quality_checks(source_name, records, quality_rules)

    # ------------------------------------------------------------------
    # Metrics
    # ------------------------------------------------------------------
    record_success(source_name)

    return records
