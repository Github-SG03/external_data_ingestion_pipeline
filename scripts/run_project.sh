##############################################################################################################
                # Load Airflow environment (NO sudo, NO installs)# Airflow ETL – EC2 Setup Script
                                                  # ./run_project.sh
##############################################################################################################
#!/bin/bash
set -e

echo "1️⃣ Activate Airflow env"
source ~/airflow_env/bin/activate

export AIRFLOW_HOME=/home/ec2-user/airflow
export AIRFLOW__CORE__DAGS_FOLDER=$AIRFLOW_HOME/dags
export ENV=dev

echo "2️⃣ Prepare Airflow directories"
mkdir -p $AIRFLOW_HOME/{dags,logs,src,config}

echo "3️⃣ Install dependencies"
pip install --no-cache-dir -r requirements.txt

echo "4️⃣ Install project package (IMPORTANT)"
pip install -e .

echo "5️⃣ Sync DAGs"
rsync -av --delete dags/ $AIRFLOW_HOME/dags/

echo "6️⃣ Sync src"
rsync -av --delete src/ $AIRFLOW_HOME/src/

echo "7️⃣ Sync config"
rsync -av config/ $AIRFLOW_HOME/config/

echo "8️⃣ Initialize / migrate Airflow DB"
airflow db migrate

echo "9️⃣ Kill old Airflow"
pkill -f "airflow scheduler" || true
pkill -f "airflow webserver" || true
sleep 5

echo "🔟 Start Airflow services"
nohup airflow scheduler > $AIRFLOW_HOME/scheduler.log 2>&1 &
nohup airflow dag-processor > $AIRFLOW_HOME/dag-processor.log 2>&1 &
nohup airflow api-server --port 8080 > $AIRFLOW_HOME/api-server.log 2>&1 &

echo "⏳ Waiting for Airflow API server..."
for i in {1..50}; do
  if curl -sf http://localhost:8080/api/v1/health > /dev/null; then
    echo "✅ Airflow API server is healthy"
    break
  fi
  sleep 5
done

echo "🧪 Checking DAG import errors"
IMPORT_ERRORS=$(airflow dags list-import-errors | wc -l)
if [ "$IMPORT_ERRORS" -gt 1 ]; then
  airflow dags list-import-errors
  echo "❌ DAG import errors found"
  exit 1
fi

echo "✅ Deployment successful"

#######################################################PROJECT EXECUTION STEPS################################

#BROWSER: http://ec2-43-204-235-11.ap-south-1.compute.amazonaws.com:8080


#ssh -i github_actions_key ec2-user@43.204.235.11(Terminal 1)
#cd external_data_ingestion_pipeline
#source ~/airflow_env/bin/activate
#export AIRFLOW_HOME=~/airflow
#export PYTHONPATH=~/airlow/src
#export ENV=dev
#airflow variables get SLACK_WEBHOOK
#pkill -9 -f airflow || true
#pkill -9 -f gunicorn || true
#pkill -9 -f uvicorn || true
#sleep 5
#ps aux | grep airflow | grep -E "scheduler|dag-processor|api-server"
#ss -lntp | grep 8080
#curl http://localhost:8080/api/v2/health
#airflow dags list-import-errors
#airflow dags list | grep github_ingestion
#airflow dags trigger github_ingestion
#airflow dags list-runs github_ingestion
#airflow tasks state github_ingestion github_etl manual__2025-12-28T14:40:09.934614+00:00_z8YHdRAY
#aws s3 ls s3://<your-bucket>/github/date=YYYY-MM-DD/
#nano ~/airflow/dags/github_ingestion_dag.py
#nano ~/airflow/src/github_pipeline/slack_alert.py



#(terminal2:CMD)
#git status
# git add .
#git commit --allow-empty -m ""
#git push -u origin main

#########################################WORKFLOW ###################################################################

#🔁 HOW CD ACTUALLY WORKS (SIMPLE):FLOW DIAGRAM
#You (Local)-GitHub push
#  |
#  | git push
#  v
#GitHub Actions SSH → EC2
#  |
#  | CI-CD workflow runs
#   v
#EC2 (via SSH)
#  |
#   | git pull
#   | Sync DAGs & plugins
#   | restart airflow:Check DAG import errors ❌/✅
#   |Health check on port 8080
#   v   
#Deployment SUCCESS  
   
#👉 EC2 is passive
#👉 GitHub connects TO EC2
#👉 EC2 does not push anything




                                            #OR#
#1.git status --Make sure everything is committed (LOCALLY)
#2.git push origin main  --Push code to GitHub (LOCALLY)
#3.Open GitHub → Actions tab  ---Verify GitHub Actions	
#4.cd ~/external_data_ingestion_pipeline
#git log --oneline -3 --Verify DAG copied to Airflow
#5.ls ~/airflow/dags --This proves rsync worked
#6.ps aux | grep airflow | grep -v grep --Verify Airflow processes
#7.ss -lntp | grep 8080 --Verify port is listening
#8.http://<EC2-PUBLIC-IP>:8080  --open Aifow ui
#9.DAG name: github_ingestion --Verify DAG
#10.airflow dags trigger github_ingestion  --Trigger DAG
#11.cd ~/airflow/logs/dag_id=github_ingestion --verigy logs
#ls
#12.SLACK MESSAGE (FINAL PROOF)






##########################################Crdentials & Link##################################################
#Username: admin
#Password: spM3QHV5xwUFythk
#http://127.0.0.1:8080

#Username: admin
#Password: sgs99@grafana
#http://43.204.235.11:9090/  Prometheus
#http://43.204.235.11:3000/  Grafana
#curl http://localhost:9100/metrics





##########################################################################################




