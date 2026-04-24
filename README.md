# GCP Project: Cricket Statistics Pipeline

## Overview
This project implements an end-to-end data pipeline to collect, transform, and visualize cricket statistics using Google Cloud Platform (GCP) services. Data is fetched from the Cricbuzz API, loaded directly into BigQuery, transformed using SQL into analytics-ready tables, and visualized in Looker.

## Architecture

```
Cricbuzz API
     │
     ▼
Python (extract_data.py)
     │  fetch & load
     ▼
BigQuery — raw_cricket (raw layer)
     │
     ├──► country_performance  (aggregated by country)
     ├──► top_players          (top 10 ranked players)
     └──► rank_distribution    (rank group breakdown)
                │
                ▼
             Looker
        (interactive dashboard)
```

The pipeline is orchestrated by Cloud Composer (managed Airflow) and runs on a daily schedule.

## Pipeline Components

1. **Python (`extract_data.py`)**: Fetches cricket statistics from the Cricbuzz API and loads them directly into BigQuery as a raw table.
2. **Cloud Composer**: Orchestrates the full pipeline — triggers the Python script and runs SQL transformation tasks in parallel.
3. **BigQuery**: Serves as both the raw data store and the analytics layer. SQL transformations produce three analytics tables from the raw data.
4. **SQL (`transform.sql`)**: Three transformation queries that build aggregated, filtered, and grouped tables for analytics use cases.
5. **Looker**: Visualizes the analytics tables through interactive dashboards.

## BigQuery Table Structure

| Table | Description |
|---|---|
| `raw_cricket` | Raw data loaded directly from the API |
| `country_performance` | Total players and average rank per country |
| `top_players` | Players ranked in the top 10 |
| `rank_distribution` | Player count grouped by Top 5 / Top 10 / Others |

## Requirements
- Google Cloud account
- Access to the Cricbuzz API
- GCP services enabled: Cloud Composer, BigQuery, Looker

## Installation

1. **Set up GCP project**: Create a new GCP project and enable the required APIs.
2. **Cloud Composer**: Set up a Cloud Composer environment for workflow orchestration.
3. **BigQuery dataset**: Create a BigQuery dataset to store raw and transformed data.
4. **Configure `config.json`**: Add your API credentials and BigQuery project/dataset details:
    ```json
    {
        "api": {
            "url": "your-api-url",
            "query_params": {},
            "headers": {}
        },
        "bigquery": {
            "project_id": "your-gcp-project-id",
            "dataset_id": "your_dataset"
        }
    }
    ```
5. **Update `dag.py`**: Set `PROJECT_ID` and `DATASET_ID` to match your GCP project.
6. **Install dependencies**: `pip install -r requirement.txt`
7. **Looker setup**: Connect Looker to BigQuery for data visualization.

## Usage

1. **Run the pipeline**: Trigger the DAG via Cloud Composer — it runs automatically on a daily schedule.
2. **View raw data**: Check `raw_cricket` in BigQuery after the fetch task completes.
3. **View analytics tables**: Check `country_performance`, `top_players`, and `rank_distribution` after the transformation tasks complete.
4. **Visualize data**: Use Looker to explore the analytics tables through the dashboard.

<img width="1438" alt="looker" src="https://github.com/user-attachments/assets/39f643d9-8f5b-405e-a654-2c791eb1f1fb">
