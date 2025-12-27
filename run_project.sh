##############################################################################################################
                # Load Airflow environment (NO sudo, NO installs)# Airflow ETL – EC2 Setup Script
                                                  # ./run_project.sh
##############################################################################################################
#!/bin/bash
#!/bin/bash
set -e

echo "1️⃣ Set Airflow environment"
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

echo "7️⃣ Kill old Airflow"
pkill -f "airflow scheduler" || true
pkill -f "airflow webserver" || true
pkill -9 -f gunicorn || true
pkill -9 -f uvicorn || true
sleep 5

echo "▶ Start Airflow (scheduler + webserver)"
nohup airflow scheduler > $AIRFLOW_HOME/scheduler.log 2>&1 </dev/null &
nohup airflow webserver > $AIRFLOW_HOME/webserver.log 2>&1 </dev/null &

sleep 10
echo "✅ Airflow restarted successfully"


#######################################################PROJECT EXECUTION STEPS################################

#ssh -i "ec2_etl_instance.pem" -L 8080:127.0.0.1:8080 ec2-user@ec2-43-204-235-11.ap-south-1.compute.amazonaws.com(Terminal 1)
#http://ec2-43-204-235-11.ap-south-1.compute.amazonaws.com:8080
#ssh -i "%USERPROFILE%\.ssh\id_ed25519" ec2-user@43.204.235.11




#ssh -i github_actions_key ec2-user@43.204.235.11(Terminal 2)
#cd external_data_ingestion_pipeline
#source ~/airflow_env/bin/activate
#export AIRFLOW_HOME=~/airflow
#export PYTHONPATH=$AIRFLOW_HOME/plugins
#export ENV=dev
#airflow variables get SLACK_WEBHOOK
#pkill -9 -f airflow || true
#pkill -9 -f gunicorn || true
#pkill -9 -f uvicorn || true
#sleep 5
#ps aux | grep airflow | grep -v grep  --main to check if all airflow processes  is  killed or  not 
#airflow dags list-import-errors
#airflow dags list | grep github_ingestion
#airflow dags trigger github_ingestion   datetime.utcnow().strftime("%Y-%m-%d")
#airflow dags list-runs github_ingestion
#airflow tasks state github_ingestion github_etl manual__2025-12-24T19:18:05+00:00
#aws s3 ls s3://<your-bucket>/github/date=YYYY-MM-DD/
#nano ~/airflow/dags/github_ingestion_dag.py
#nano ~/airflow/plugins/github_pipeline/slack_alert.py




#ssh -i github_actions_key ec2-user@43.204.235.11(Terminal 3)
#cd external-data-ingestion-pipeline
##./run_project.sh

############################################################################################################





##########################################Crdentials & Link##################################################
#Username: admin
#Password: spM3QHV5xwUFythk
#http://127.0.0.1:8080

#Username: admin
#Password: sgs99@grafana
#http://43.204.235.11:9090/  Prometheus
#http://43.204.235.11:3000/  Grafana

#🔁 HOW CD ACTUALLY WORKS (SIMPLE)
#FLOW DIAGRAM
#You (Local)
#   |
#   | git push
#  v
#GitHub
#  |
#   | CD workflow runs
#   v
#EC2 (via SSH)
#  |
#   | git pull
#   | restart airflow


#👉 EC2 is passive
#👉 GitHub connects TO EC2
#👉 EC2 does not push anything







