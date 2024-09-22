# GCP Project: Cricket Statistics Pipeline

## Overview
This project implements a data pipeline to collect, process, and visualize cricket statistics using Google Cloud Platform (GCP) services. The data is fetched from the Cricbuzz API, processed using Dataflow, and visualized in Looker.

## Architecture
<img width="634" alt="architecture" src="https://github.com/user-attachments/assets/b4249d29-6311-465b-a512-632e75f79aee">

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

<img width="1438" alt="looker" src="https://github.com/user-attachments/assets/39f643d9-8f5b-405e-a654-2c791eb1f1fb">

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
