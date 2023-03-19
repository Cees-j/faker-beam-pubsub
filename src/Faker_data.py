from google.cloud import pubsub_v1
from faker import Faker
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

PROJECT_ID = os.getenv('PROJECT_ID')
TOPIC_NAME = os.getenv('TOPIC_NAME')
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path


publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()


def push_faker_data(publisher=publisher):
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
    faker = Faker()

    # Generate and publish simulated IoT data
    print('Publishing faker data')
    for i in range(300):
        data = {
            'device_id': faker.uuid4(),
            'temperature': faker.random_int(min=20, max=40),
            'humidity': faker.random_int(min=30, max=70),
            'timestamp': datetime.now().isoformat()
        }
        print(data)
        message = json.dumps(data).encode('utf-8')
        future = publisher.publish(topic_path, data=message)
        print(future.result())

    print('Published messages to Pub/Sub topic.')

push_faker_data(publisher=publisher)


