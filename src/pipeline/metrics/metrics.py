from prometheus_client import Counter, Histogram

# Total records ingested per source
RECORDS_INGESTED = Counter(
    "records_ingested_total", "Total records ingested", ["source"]
)

# Source failures
SOURCE_FAILURES = Counter(
    "source_failures_total", "Total ingestion failures", ["source"]
)

# Execution duration
INGESTION_DURATION = Histogram(
    "ingestion_duration_seconds", "Ingestion duration per source", ["source"]
)


def record_success(source: str, count: int, duration: float):
    RECORDS_INGESTED.labels(source=source).inc(count)
    INGESTION_DURATION.labels(source=source).observe(duration)


def record_failure(source: str):
    SOURCE_FAILURES.labels(source=source).inc()
