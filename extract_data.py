import requests
import json
import logging
import argparse
import pandas as pd
from google.cloud import bigquery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

with open('config.json') as config_file:
    config = json.load(config_file)

url = config['api']['url']
querystring = config['api']['query_params']
headers = config['api']['headers']
project_id = config['bigquery']['project_id']
dataset_id = config['bigquery']['dataset_id']
table_id = f"{project_id}.{dataset_id}.raw_cricket"
field_names = ['rank', 'name', 'country']


def fetch_data_from_api(url: str, headers: dict, params: dict) -> list:
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json().get('rank', [])
        if not data:
            logger.warning("API returned empty data")
            return []
        logger.info(f"Successfully fetched {len(data)} records from API")
        return data
    except requests.exceptions.Timeout:
        logger.error("API request timed out after 30 seconds")
        raise
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
        raise
    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to API")
        raise
    except (ValueError, KeyError) as e:
        logger.error(f"Failed to parse API response: {e}")
        raise


def load_to_bigquery(data: list, table_id: str, field_names: list) -> None:
    try:
        client = bigquery.Client()
        df = pd.DataFrame(
            [{field: entry.get(field) for field in field_names} for entry in data]
        )
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            schema=[
                bigquery.SchemaField("rank",    "STRING"),
                bigquery.SchemaField("name",    "STRING"),
                bigquery.SchemaField("country", "STRING"),
            ]
        )
        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()
        logger.info(f"{job.output_rows} rows loaded to {table_id}")
    except Exception as e:
        logger.error(f"Failed to load data to BigQuery: {e}")
        raise


# Each function below is independently callable from the DAG as a separate task
def task_fetch_and_load():
    data = fetch_data_from_api(url, headers, querystring)
    if not data:
        raise ValueError("No data fetched from API")
    load_to_bigquery(data, table_id, field_names)
    logger.info("fetch_and_load task completed")


if __name__ == "__main__":
    # Accepts a task argument so each step can be triggered individually from the DAG
    parser = argparse.ArgumentParser()
    parser.add_argument('task', choices=['fetch'])
    args = parser.parse_args()

    if args.task == 'fetch':
        task_fetch_and_load()
