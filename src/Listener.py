from google.cloud import pubsub_v1
import json
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv('PROJECT_ID')
SUB_NAME = os.getenv('SUB_NAME')
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path



subscriber = pubsub_v1.SubscriberClient()

def callback(message):
    print(f"Received message: {message}")
    message.ack()

def start_message_listener(project_id, subscription_name, callback, subscriber=subscriber):
    ''' Subscribed to the topic and subscription we made, and its listening for any faker_data that gets published'''
    print('Starting to listen')

    # Create the subscription path
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    # Subscribe to the subscription and start the message listener
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    # Block the current thread until the message listener is stopped
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()

    return "Message listener stopped."

start_message_listener(PROJECT_ID, SUB_NAME, callback=callback, subscriber=subscriber)

