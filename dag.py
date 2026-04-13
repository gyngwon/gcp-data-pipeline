from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.sensors.bigquery import BigQueryTableExistenceSensor

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 22),
    'depends_on_past': False,
    'email': ['ruddnjs0366@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

SCRIPT_PATH = '/home/airflow/gcs/dags/scripts/extract_data.py'

with DAG(
    dag_id='fetch_cricket_stats',
    default_args=default_args,
    description='Cricket stats pipeline: fetch → GCS → Dataflow → BigQuery',
    schedule_interval='@daily',
    catchup=False,
    tags=['cricket', 'gcp'],
) as dag:

    # Task 1: Fetch data from API and save as CSV
    fetch_data = BashOperator(
        task_id='fetch_data',
        bash_command=f'python {SCRIPT_PATH} fetch',
    )

    # Task 2: Upload CSV file to GCS
    upload_to_gcs = BashOperator(
        task_id='upload_to_gcs',
        bash_command=f'python {SCRIPT_PATH} upload',
    )

    # Task 3: Wait for BigQuery table to be loaded
    # Cloud Functions automatically triggers Dataflow on GCS upload event
    wait_for_bq_load = BigQueryTableExistenceSensor(
        task_id='wait_for_bq_load',
        project_id='your-gcp-project-id',
        dataset_id='your_dataset',
        table_id='icc_odi_batsmen_ranking',
        timeout=600,        # wait up to 10 minutes
        poke_interval=30,   # check every 30 seconds
    )

    # Task 4: Log pipeline completion
    pipeline_complete = BashOperator(
        task_id='pipeline_complete',
        bash_command='echo "Pipeline completed at $(date)"',
    )

    # Define task execution order
    fetch_data >> upload_to_gcs >> wait_for_bq_load >> pipeline_complete
