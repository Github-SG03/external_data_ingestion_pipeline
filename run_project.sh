#!/bin/bash
set -e

echo "1️⃣ Activate Airflow env"
source ~/airflow_env/bin/activate

export AIRFLOW_HOME=/home/ec2-user/airflow
export AIRFLOW__CORE__DAGS_FOLDER=$AIRFLOW_HOME/dags
export PYTHONPATH=$AIRFLOW_HOME/plugins
export ENV=dev

echo "2️⃣ Prepare Airflow directories"
mkdir -p $AIRFLOW_HOME/{dags,plugins,logs,config}

echo "3️⃣ Install dependencies"
pip install --no-cache-dir -r requirements.txt

echo "4️⃣ Sync DAGs"
rsync -av --delete dags/ $AIRFLOW_HOME/dags/

echo "5️⃣ Sync plugins"
rsync -av --delete plugins/ $AIRFLOW_HOME/plugins/

echo "6️⃣ Sync config"
rsync -av config/ $AIRFLOW_HOME/config/

echo "7️⃣ Initialize / migrate Airflow DB"
airflow db migrate

echo "8⃣ Checking DAG import errors (FAIL FAST)"
IMPORT_ERRORS=$(airflow dags list-import-errors | wc -l)

if [ "$IMPORT_ERRORS" -gt 1 ]; then
  echo "❌ DAG import errors detected. Aborting deployment."
  airflow dags list-import-errors
  exit 1
else
  echo "✅ No DAG import errors found"
fi

echo "9️⃣ Kill old Airflow"
pkill -f "airflow scheduler" || true
pkill -f "airflow webserver" || true
sleep 5

echo "🔟 Start Airflow"
nohup airflow scheduler > $AIRFLOW_HOME/scheduler.log 2>&1 &
nohup airflow webserver --port 8080 > $AIRFLOW_HOME/webserver.log 2>&1 &

sleep 20

echo "🔍 Checking Airflow health"
curl -f http://localhost:8080/health || {
  echo "❌ Airflow health check failed"
  exit 1
}

echo "✅ Airflow is healthy"
exit 0
