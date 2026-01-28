import time


def retry(operation, retries=3, delay=10):
    for attempt in range(1, retries + 1):
        try:
            return operation()
        except Exception as e:
            if attempt == retries:
                raise
            time.sleep(delay)
