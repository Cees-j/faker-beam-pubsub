from google.cloud import pubsub_v1
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv('PROJECT_ID')
TOPIC_NAME = os.getenv('TOPIC_NAME')
SUB_NAME = os.getenv('SUB_NAME')
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()


def create_pubsub_topic(project_id, topic_name):
    """Create a new Pub/Sub topic in the specified GCP project"""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    try:
        topic = publisher.create_topic(request={"name": topic_path})
        print(f"Created topic: {topic.name}")
    except Exception as e:
        topic = publisher.get_topic(request={"topic": topic_path})
        print(f"Topic already exists: {topic.name}")
    return topic

create_pubsub_topic(PROJECT_ID, TOPIC_NAME)


def create_pubsub_subscription(project_id, topic_name, subscription_name, publisher=publisher, subscriber=subscriber):
    ''' After creating a topic, now we create a subscription that a service can subscribe to '''
    topic_path = publisher.topic_path(project_id, topic_name)
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    try:
        print('Trying to create subscription')
        # Try to create the subscription
        subscription = subscriber.create_subscription(request={"name": subscription_path, "topic": topic_path})
        print(f'Subscription created to {project_id} {topic_name}')
        return subscription.name
    except Exception as e:
        # Handle exceptions and provide meaningful error messages
        error_message = f"Error creating subscription '{subscription_name}' for topic '{topic_name}': {str(e)}"
        print(error_message)
        return None

create_pubsub_subscription(PROJECT_ID, TOPIC_NAME, SUB_NAME, publisher=publisher, subscriber=subscriber)
