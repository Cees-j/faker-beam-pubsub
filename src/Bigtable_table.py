import subprocess

project_id = 'my-faker-beam'
instance_id = "cbt-faker-instance-id"
table_id = "your-table-id"

# Construct the command to create the table
#cmd = f"gcloud bigtable createtable {table_id} --instance={instance_id} --cluster=cluster-1 --project={project_id}".split()
cmd = f"gcloud bigtable instances tables create {table_id} --instance={instance_id} --column-families=my-family".split()
# Run the command using subprocess
try:
    subprocess.run(cmd, check=True)
    print(f"Table {table_id} created successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error creating table {table_id}: {e}")

