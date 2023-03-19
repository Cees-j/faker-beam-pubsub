import pandas as pd 
import os
import argparse
import json
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromPubSub
from apache_beam.io.gcp.bigtableio import WriteToBigTable
from apache_beam.options.pipeline_options import StandardOptions
from google.cloud.bigtable import Client, row
from dotenv import load_dotenv

load_dotenv()
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
# Define the command-line arguments for your pipeline:


parser = argparse.ArgumentParser()
parser.add_argument('--project', help='GCP project ID')
parser.add_argument('--topic', help='Pub/Sub topic name')
parser.add_argument('--subscription', help='Pub/Sub subscription name')
parser.add_argument('--bigtable_instance', help='Bigtable instance ID')
parser.add_argument('--bigtable_table', help='Bigtable table ID')
args, pipeline_args = parser.parse_known_args()

def run_pipeline(args, pipeline_args):
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(StandardOptions).streaming = True

    with beam.Pipeline(options=pipeline_options) as pipeline:
        # Read data from Pub/Sub
        messages = (
            pipeline
            | 'Read from Pub/Sub' >> ReadFromPubSub(subscription=args.subscription)
            | 'Decode messages' >> beam.Map(json.loads)
        )

        messages | 'Print messages' >> beam.Map(print)
        # Process and write data to Bigtable
        (
            messages
            | 'Convert to Bigtable rows' >> beam.Map(convert_to_bigtable_row)
            | 'Write to Bigtable' >> WriteToBigTable(
                project_id=args.project,
                instance_id=args.bigtable_instance,
                table_id=args.bigtable_table
            )
        )

def convert_to_bigtable_row(iot_data):
    print('trying to convert to bigtable row')
    print(iot_data)
    device_id = iot_data['device_id']
    temperature = iot_data['temperature']
    humidity = iot_data['humidity']
    timestamp = iot_data['timestamp']

    # Create a new row with the device_id as the row key
    bt_row = row.DirectRow(row_key=device_id.encode('utf-8'))

    # Set the column values for the row
    bt_row.set_cell('my-family', b'temperature', str(temperature).encode('utf-8'))
    bt_row.set_cell('my-family', b'humidity', str(humidity).encode('utf-8'))
    bt_row.set_cell('my-family', b'timestamp', timestamp.encode('utf-8'))

    print('returning', bt_row, type(bt_row))
    return bt_row

if __name__ == '__main__':
    run_pipeline(args, pipeline_args)

# python Beam-pipeline.py \
# --project my-faker-beam \
# --topic your-topic-name-Main-topic \
# --subscription projects/my-faker-beam/subscriptions/Subscription_name_101 \
# --bigtable_instance cbt-faker-instance-id \
# --bigtable_table your-table-id \
# --streaming
#     Replace the placeholders with the appropriate values from your earlier scripts:


    # PROJECT_ID: The value of the PROJECT_ID variable in your scripts (e.g., my-faker-beam).
    # TOPIC_NAME: The value of the TOPIC_NAME variable in your scripts (e.g., the name you used when creating the Pub/Sub topic).
    # SUB_NAME: The value of the SUB_NAME variable in your scripts (e.g., the name you used when creating the Pub/Sub subscription).
    # INSTANCE_ID: The value of the INSTANCE_ID variable in your Script 1 (e.g., cbt-faker-instance-id).
    # TABLE_ID: The value of the table_id variable in your Script 2 (e.g., your-table-id).
    # Make sure to replace the placeholders with the actual values you used in your scripts before running the command.
