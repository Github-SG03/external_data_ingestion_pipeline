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

echo "7️⃣ Checking DAG import errors (FAIL FAST)"

IMPORT_ERRORS=$(airflow dags list-import-errors | wc -l)

if [ "$IMPORT_ERRORS" -gt 1 ]; then
  echo "❌ DAG import errors detected. Aborting deployment."
  airflow dags list-import-errors
  exit 1
else
  echo "✅ No DAG import errors found"
fi


echo "8️⃣ Kill old Airflow"
pkill -f "airflow scheduler" || true
pkill -f "airflow webserver" || true
sleep 5

echo "9️⃣ Start Airflow (scheduler + webserver)"
nohup airflow scheduler > $AIRFLOW_HOME/scheduler.log 2>&1 &
nohup airflow webserver --port 8080 > $AIRFLOW_HOME/webserver.log 2>&1 &

sleep 15

echo "🔍 Checking Airflow health"
curl -f http://localhost:8080/health || {
  echo "❌ Airflow health check failed"
  exit 1
}

echo "✅ Airflow is healthy and running"
exit 0



#######################################################PROJECT EXECUTION STEPS################################

#(Terminal 1)-http://ec2-43-204-235-11.ap-south-1.compute.amazonaws.com:8080





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




##########################################################################################




