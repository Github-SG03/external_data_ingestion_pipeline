from src.pipeline.notify.slack import send_slack


def escalate(source: str, failure_count: int):
    if failure_count >= 3:
        send_slack(
            f"🚨 ESCALATION: {source} failed {failure_count} times. Immediate attention required."
        )
