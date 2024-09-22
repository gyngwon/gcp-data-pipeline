import requests
import csv
import json
from google.cloud import storage

# Load configuration from JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

# Read API and GCS configuration
url = config['api']['url']
querystring = config['api']['query_params']
headers = config['api']['headers']

# Send API request
response = requests.get(url, headers=headers, params=querystring)

if response.status_code == 200:
    data = response.json().get('rank', [])
    csv_filename = config['gcs']['csv_filename']

    if data:
        field_names = ['rank', 'name', 'country']

        # Write data to CSV file
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            for entry in data:
                writer.writerow({field: entry.get(field) for field in field_names})

        print(f"Data fetched successfully and written as '{csv_filename}'")

        # Upload the CSV file to GCS
        bucket_name = config['gcs']['bucket_name']
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        destination_blob_name = csv_filename

        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(csv_filename)

        print(f"File {csv_filename} uploaded to GCS bucket {bucket_name} as {destination_blob_name}")

    else:
        print("No data available from the API.")

else:
    print("Failed to fetch data:", response.status_code)
