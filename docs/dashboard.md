# Analytics & Dashboards

## Data Sources
The external ingestion platform lands raw data in S3, partitioned by date.

Example:
s3://company-raw-data/github/dt=YYYY-MM-DD/data.json

## Query Layer
Data is queried using:
- AWS Athena (primary)
- Snowflake (enterprise sources)

## Superset Integration
Superset connects to:
- Athena catalog
- Snowflake warehouse

## Dashboards Provided
- Ingestion volume per source
- Data freshness (last successful run)
- Failure trends
- Vendor SLA metrics

## Users
- Business analysts
- Operations teams
- Leadership
