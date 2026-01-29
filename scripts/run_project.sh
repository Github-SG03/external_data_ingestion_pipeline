##############################################################################################################
                # Load Airflow environment (NO sudo, NO installs)# Airflow ETL – EC2 Setup Script
                                                  # ./run_project.sh
##############################################################################################################
#!/bin/bash
set -e

echo "=============================="
echo "🚀 External Data Ingestion Platform – Deployment"
echo "=============================="

echo "1️⃣ Activate Airflow virtual environment"
source ~/airflow_env/bin/activate

export AIRFLOW_HOME=/home/ec2-user/airflow
export AIRFLOW__CORE__DAGS_FOLDER=$AIRFLOW_HOME/dags
export PYTHONPATH=$AIRFLOW_HOME/src
export ENV=dev

echo "2️⃣ Prepare Airflow directories"
mkdir -p $AIRFLOW_HOME/dags
mkdir -p $AIRFLOW_HOME/logs
mkdir -p $AIRFLOW_HOME/src
mkdir -p $AIRFLOW_HOME/config

echo "3️⃣ Upgrade pip"
pip install --upgrade pip

echo "4️⃣ Install Python dependencies"
pip install --no-cache-dir -r requirements.txt

echo "5️⃣ Clean old editable installs (SAFE)"
pip uninstall -y github_pipeline || true
pip uninstall -y external_data_ingestion_pipeline || true
rm -f $AIRFLOW_HOME/venv/lib/python*/site-packages/_editable__*.pth || true

echo "6️⃣ Install project package (editable)"
pip install -e .

echo "7️⃣ Sync DAGs to Airflow"
rsync -av --delete dags/ $AIRFLOW_HOME/dags/

echo "8️⃣ Sync source code"
rsync -av --delete src/ $AIRFLOW_HOME/src/

echo "9️⃣ Sync config files"
rsync -av config/ $AIRFLOW_HOME/config/

echo "🔟 Initialize / migrate Airflow DB"
airflow db migrate

echo "1️⃣1️⃣ Stop old Airflow processes"
pkill -f "airflow scheduler" || true
pkill -f "airflow dag-processor" || true
pkill -f "airflow api-server" || true
sleep 5

echo "1️⃣2️⃣ Start Airflow services"
nohup airflow scheduler > $AIRFLOW_HOME/scheduler.log 2>&1 &
nohup airflow dag-processor > $AIRFLOW_HOME/dag-processor.log 2>&1 &
nohup airflow api-server --port 8080 > $AIRFLOW_HOME/api-server.log 2>&1 &

echo "1️⃣3️⃣ Wait for Airflow API health check"
for i in {1..60}; do
  if curl -sf http://localhost:8080/api/v1/health > /dev/null; then
    echo "✅ Airflow API server is healthy"
    break
  fi
  sleep 5
done

echo "1️⃣4️⃣ Check DAG import errors"
IMPORT_ERRORS=$(airflow dags list-import-errors | wc -l)
if [ "$IMPORT_ERRORS" -gt 1 ]; then
  echo "❌ DAG import errors detected"
  airflow dags list-import-errors
  exit 1
fi

echo "=============================="
echo "✅ DEPLOYMENT SUCCESSFUL"
echo "=============================="

echo "🌐 Airflow UI: http://<EC2-PUBLIC-IP>:8080"


