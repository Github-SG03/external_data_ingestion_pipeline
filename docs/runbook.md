```
# Production Runbook

## Common Issues

### Source Failure
- Check Slack alert
- Identify source
- Review Airflow logs
- Retry source if needed

### Data Missing
- Check backfill config
- Verify source availability
- Validate S3 partition

## Escalation
- Notify data platform owner
- Open incident ticket

```
