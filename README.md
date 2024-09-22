# GCP Project: BigQuery - Cricket Statistics Pipeline

## Overview
This project implements a data pipeline to collect, process, and visualize cricket statistics using Google Cloud Platform (GCP) services. The data is fetched from the Cricbuzz API, processed using Dataflow, and visualized in Looker.

## Architecture
The architecture consists of the following components:

1. **Data Collection**: Fetches cricket statistics from the Cricbuzz API using Python.
2. **Cloud Composer**: Orchestrates the data pipeline and schedules data fetching.
3. **Cloud Storage**: Stores fetched data in CSV format within a Google Cloud Storage (GCS) bucket.
4. **Cloud Functions**: Automatically triggers processing jobs upon new file uploads to GCS.
5. **Dataflow**: Processes and transforms the data from the CSV files.
6. **BigQuery**: Stores the processed data in a serverless data warehouse for scalable querying.
7. **Looker**: Visualizes data insights through interactive dashboards.

## Requirements
- Google Cloud account
- Access to the Cricbuzz API
- GCP services enabled: Cloud Composer, Cloud Storage, Cloud Functions, Dataflow, BigQuery, Looker

## Installation
1. **Set Up GCP Project**: Create a new GCP project and enable the required APIs.
2. **Cloud Composer**: Set up a Cloud Composer environment for workflow orchestration.
3. **Cloud Storage**: Create a GCS bucket for temporary data storage.
4. **Cloud Functions**: Write and deploy functions to trigger Dataflow jobs.
5. **Dataflow Jobs**: Implement Dataflow pipelines to process the CSV files.
6. **BigQuery Dataset**: Create a BigQuery dataset to store processed data.
7. **Looker Setup**: Connect Looker to BigQuery for data visualization.

## Usage
1. **Run the Data Pipeline**: Trigger the data collection via Cloud Composer.
2. **View Processed Data**: Check the BigQuery dataset for the processed cricket statistics.
3. **Visualize Data**: Use Looker to create dashboards and explore the data.

## Code Snippet

Here’s an example of how to fetch data from the Cricbuzz API and store it as a CSV file:

```python
import requests
import pandas as pd

# Fetch data from Cricbuzz API
url = 'https://example.com/api/cricket'  # Replace with actual Cricbuzz API URL
response = requests.get(url)
data = response.json()

# Convert to DataFrame and save as CSV
df = pd.DataFrame(data)
df.to_csv('cricket_stats.csv', index=False)
