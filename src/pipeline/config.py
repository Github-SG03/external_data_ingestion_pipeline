import os
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

def get_env() -> str:
    return os.getenv("ENV", "dev")

def _load_yaml(path: str) -> dict:
    full_path = BASE_DIR / path
    if not full_path.exists():
        raise FileNotFoundError(f"Config not found: {full_path}")
    with open(full_path, "r") as f:
        return yaml.safe_load(f) or {}

def load_sources() -> list:
    env = get_env()
    cfg = _load_yaml(f"config/sources.{env}.yaml")
    return cfg.get("sources", [])

def load_backfill_config() -> dict:
    return _load_yaml("config/backfill.yaml")

def load_quality_rules() -> dict:
    return _load_yaml("config/quality_rules.yaml")
