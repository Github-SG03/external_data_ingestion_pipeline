<<<<<<< Updated upstream
![CI](https://github.com/Github-SG03/external_data_ingestion_pipeline/actions/workflows/ci.yml/badge.svg)
>>>>>>> Stashed changes
## External Data Ingestion Pipeline(v1)


## Overview
Production-ready data ingestion pipeline using Apache Airfow 3, Deployed on AWS EC2

## Architecture
Github->Github Actions->EC2->Airflow->S3->Slack

## Tech Stack
- Apache Airflow 3
- Python 3.0
- AWS EC2 + S3
- Github Actions
- Slack Alerts
- Prometheus + Grafana(Infra Monitoring)


## Dags
- github_ingestion
  - Extracts Github Data
  - Writes Partitioned CSV to S3
  - Sends Slack Alerts on succes/failure


## S3 Outputs
s3://sgs-dev-data-bucket/github/dev/date=YYYY-MM-DD/


## CICD
- Linting
- Dag Import Validation
- EC2 Deployment via ssh
- Health Checks


## Monitoring
- Node exporter( CPU/Memory/Disk)
- Prometheus
- Grafana Dashboards


##Status
Production Stable(tag:v10.0-airflow_prod_demo)

