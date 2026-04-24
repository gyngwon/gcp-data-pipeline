from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

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
PROJECT_ID  = 'your-gcp-project-id'
DATASET_ID  = 'your_dataset'

with DAG(
    dag_id='fetch_cricket_stats',
    default_args=default_args,
    description='Cricket stats pipeline: API → BigQuery raw → SQL transforms → analytics tables',
    schedule_interval='@daily',
    catchup=False,
    tags=['cricket', 'gcp'],
) as dag:

    # Task 1: Fetch data from API and load directly into BigQuery raw table
    fetch_and_load = BashOperator(
        task_id='fetch_and_load',
        bash_command=f'python {SCRIPT_PATH} fetch',
    )

    # Task 2: Build country-level aggregation table
    transform_country = BigQueryInsertJobOperator(
        task_id='transform_country_performance',
        configuration={
            "query": {
                "query": f"""
                    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.country_performance` AS
                    SELECT
                        country,
                        COUNT(*) AS total_players,
                        AVG(CAST(rank AS INT64)) AS avg_rank
                    FROM `{PROJECT_ID}.{DATASET_ID}.raw_cricket`
                    GROUP BY country
                """,
                "useLegacySql": False,
            }
        },
        gcp_conn_id='google_cloud_default',
    )

    # Task 3: Build top 10 players table
    transform_top_players = BigQueryInsertJobOperator(
        task_id='transform_top_players',
        configuration={
            "query": {
                "query": f"""
                    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.top_players` AS
                    SELECT
                        name,
                        country,
                        CAST(rank AS INT64) AS rank
                    FROM `{PROJECT_ID}.{DATASET_ID}.raw_cricket`
                    WHERE CAST(rank AS INT64) <= 10
                """,
                "useLegacySql": False,
            }
        },
        gcp_conn_id='google_cloud_default',
    )

    # Task 4: Build rank distribution table
    transform_rank_dist = BigQueryInsertJobOperator(
        task_id='transform_rank_distribution',
        configuration={
            "query": {
                "query": f"""
                    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.rank_distribution` AS
                    SELECT
                        CASE
                            WHEN CAST(rank AS INT64) <= 5  THEN 'Top 5'
                            WHEN CAST(rank AS INT64) <= 10 THEN 'Top 10'
                            ELSE 'Others'
                        END AS rank_group,
                        COUNT(*) AS count
                    FROM `{PROJECT_ID}.{DATASET_ID}.raw_cricket`
                    GROUP BY rank_group
                """,
                "useLegacySql": False,
            }
        },
        gcp_conn_id='google_cloud_default',
    )

    # Task 5: Log pipeline completion
    pipeline_complete = BashOperator(
        task_id='pipeline_complete',
        bash_command='echo "Pipeline completed at $(date)"',
    )

    # Transform tasks run in parallel after raw load completes
    fetch_and_load >> [transform_country, transform_top_players, transform_rank_dist] >> pipeline_complete
