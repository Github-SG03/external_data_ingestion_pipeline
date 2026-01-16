def get_required_columns(rule_cfg: dict) -> list:
    return rule_cfg.get("required_columns", [])

def get_min_rows(rule_cfg: dict) -> int:
    return rule_cfg.get("min_rows", 0)

def is_hard_fail(rule_cfg: dict) -> bool:
    return rule_cfg.get("hard_fail", False)
