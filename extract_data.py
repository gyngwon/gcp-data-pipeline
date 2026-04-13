import requests
import csv
import json
import logging
import argparse
from google.cloud import storage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

with open('config.json') as config_file:
    config = json.load(config_file)

url = config['api']['url']
querystring = config['api']['query_params']
headers = config['api']['headers']
csv_filename = config['gcs']['csv_filename']
bucket_name = config['gcs']['bucket_name']
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

def write_to_csv(data: list, csv_filename: str, field_names: list) -> None:
    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            for entry in data:
                writer.writerow({field: entry.get(field) for field in field_names})
        logger.info(f"Data written to {csv_filename}")
    except IOError as e:
        logger.error(f"Failed to write CSV file: {e}")
        raise

def upload_to_gcs(csv_filename: str, bucket_name: str) -> None:
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(csv_filename)
        blob.upload_from_filename(csv_filename)
        logger.info(f"File {csv_filename} uploaded to GCS bucket {bucket_name}")
    except Exception as e:
        logger.error(f"Failed to upload to GCS: {e}")
        raise

# Each function below is independently callable from the DAG as a separate task
def task_fetch_and_save():
    data = fetch_data_from_api(url, headers, querystring)
    if not data:
        raise ValueError("No data fetched from API")
    write_to_csv(data, csv_filename, field_names)
    logger.info("fetch_and_save task completed")

def task_upload_to_gcs():
    upload_to_gcs(csv_filename, bucket_name)
    logger.info("upload_to_gcs task completed")

if __name__ == "__main__":
    # Accepts a task argument so each step can be triggered individually from the DAG
    parser = argparse.ArgumentParser()
    parser.add_argument('task', choices=['fetch', 'upload', 'all'])
    args = parser.parse_args()

    if args.task == 'fetch':
        task_fetch_and_save()
    elif args.task == 'upload':
        task_upload_to_gcs()
    elif args.task == 'all':
        task_fetch_and_save()
        task_upload_to_gcs()
