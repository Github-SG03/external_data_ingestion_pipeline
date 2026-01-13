import os


class PipelineMetrics:
    def __init__(self, name: str):
        self.file = f"{os.environ['AIRFLOW_HOME']}/logs/{name}_metrics.prom"

    def increment(self, metric: str):
        with open(self.file, "a") as f:
            f.write(f"{metric} 1\n")
            metrics.increment("rows_written", len(df))
            metrics.increment("s3_uploads_total")

