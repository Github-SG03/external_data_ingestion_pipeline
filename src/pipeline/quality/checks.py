def check_not_empty(records: list) -> bool:
    return len(records) > 0


def check_min_rows(records: list, min_rows: int) -> bool:
    return len(records) >= min_rows


def check_required_columns(records: list, required_columns: list) -> bool:
    if not records:
        return False
    sample = records[0]
    return all(col in sample for col in required_columns)
