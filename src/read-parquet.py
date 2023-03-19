import pandas as pd
import pyarrow.parquet as pq
from google.cloud import storage
' after taking data from bigtable storing it in gcs, this will download the parquet file'
# Define GCS credentials and bucket information
project_id = 'my-faker-beam'
bucket_name = 'ex1ceesbuck'
credentials_path = 'credentials.json'

# Set the name of the file you want to download (including the file extension)
filename = 'cloud-bigtable-cbt-faker-instance-id-your-table-id-00000-of-00002.parquet'

# Set the path to write the CSV file to
output_path = 'dog.csv'

# Initialize GCS client
storage_client = storage.Client.from_service_account_json(credentials_path)

# Get bucket and file objects
bucket = storage_client.get_bucket(bucket_name)
blob = bucket.blob(filename)

# Download file to a temporary location
temp_file = '/tmp/temp.parquet'
blob.download_to_filename(temp_file)

# Read Parquet file using PyArrow
table = pq.read_table(temp_file)
df = table.to_pandas()

# Write dataframe to CSV file
df.to_csv(output_path, index=False)
