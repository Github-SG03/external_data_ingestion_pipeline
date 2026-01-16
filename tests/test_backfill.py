from src.pipeline.backfill import get_run_dates

def test_backfill_disabled():
    cfg = {"enabled": False}
    dates = get_run_dates(cfg)
    assert len(dates) == 1
