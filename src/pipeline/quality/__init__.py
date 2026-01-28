from src.pipeline.quality.checks import (
    check_not_empty,
    check_min_rows,
    check_required_columns,
)
from src.pipeline.quality.rules import (
    get_required_columns,
    get_min_rows,
    is_hard_fail,
)


class DataQualityException(Exception):
    pass


def run_quality_checks(source_name: str, records: list, rule_cfg: dict):
    """
    Runs quality checks.
    Fails hard only if configured.
    """
    failures = []

    if not check_not_empty(records):
        failures.append("Dataset is empty")

    min_rows = get_min_rows(rule_cfg)
    if min_rows and not check_min_rows(records, min_rows):
        failures.append(f"Row count below minimum: {min_rows}")

    required_cols = get_required_columns(rule_cfg)
    if required_cols and not check_required_columns(records, required_cols):
        failures.append(f"Missing required columns: {required_cols}")

    if failures:
        if is_hard_fail(rule_cfg):
            raise DataQualityException(f"[HARD FAIL] {source_name}: {failures}")
        else:
            # Soft fail: log + continue
            print(f"[DQ WARNING] {source_name}: {failures}")
