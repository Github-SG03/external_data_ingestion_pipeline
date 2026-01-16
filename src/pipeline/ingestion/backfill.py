from datetime import datetime, timedelta

def generate_dates(start_date: str, end_date: str):
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)

    while start <= end:
        yield start.strftime("%Y-%m-%d")
        start += timedelta(days=1)
