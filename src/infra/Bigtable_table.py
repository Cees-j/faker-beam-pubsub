import subprocess
import os 
from dotenv import load_dotenv

load_dotenv()

project_id = 'my-faker-beam'
INSTANCE_ID = "cbt-faker-instance-id"
table_id = "your-table-id"

# Construct the command to create the table
cmd = f"gcloud bigtable instances tables create {table_id} --instance={INSTANCE_ID} --column-families=my-family".split()
# Run the command using subprocess
try:
    subprocess.run(cmd, check=True)
    print(f"Table {table_id} created successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error creating table {table_id}: {e}")

