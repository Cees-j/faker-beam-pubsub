import subprocess
import os 
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv('PROJECT_ID')
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path


INSTANCE_ID = "cbt-faker-instance-id"
CLUSTER_ID = "cbt-faker-cluster-id"
DISPLAY_NAME = 'your-display-name'
CLUSTER_STORAGE_TYPE = 'SSD'  
CLUSTER_ZONE = 'europe-west2-a'
CLUSTER_NUM_NODES = '3'  

command = [
    'gcloud',
    'bigtable',
    'instances',
    'create',
    INSTANCE_ID,
    '--display-name={}'.format(DISPLAY_NAME),
    '--cluster-storage-type={}'.format(CLUSTER_STORAGE_TYPE),
    '--cluster-config=id={},zone={},nodes={}'.format(CLUSTER_ID, CLUSTER_ZONE, CLUSTER_NUM_NODES),
]

subprocess.run(command, check=True)