from datetime import datetime, timedelta

def get_run_dates(backfill_cfg: dict):
    """
    Returns list of dates to run.
    """
    if not backfill_cfg.get("enabled", False):
        return [datetime.utcnow().strftime("%Y-%m-%d")]

    start = datetime.fromisoformat(backfill_cfg["start_date"])
    end = datetime.fromisoformat(backfill_cfg["end_date"])

    dates = []
    while start <= end:
        dates.append(start.strftime("%Y-%m-%d"))
        start += timedelta(days=1)

    return dates
