from django.conf import settings
import concurrent.futures
from kafka import KafkaConsumer, KafkaProducer
from json import loads, dumps
from config.celery_app import app
from celery.exceptions import SoftTimeLimitExceeded
import logging

from notification_validator.notification_consumer.handler.instance_handler import SubscriptionInstanceHandlerStrategy, \
    UserInstanceHandlerStrategy
from notification_validator.notifications.models import Notification

logger = logging.getLogger()


# saves the data to the database
def persist_data(users, message, provider, ttl=1):
    Notification.objects.create(users=users, message=message, provider=provider, time_to_live=ttl)


def push_in_provider_topic(users, message, provider):
    '''
    sends the processed data to the kafka topic.
    :param users: list
    :param message: json
    :param provider: string
    '''
    producer = KafkaProducer(
        value_serializer=lambda m: dumps(m).encode('utf-8'),
        bootstrap_servers=settings.BOOTSTRAP_SERVERS_PRODUCERS)

    data = {"users": users, "message": message}
    producer.send(provider, value=data)



def fetch_user_objects(instance_handler, data):
    '''
    - sends the notification directly or persists it in the database
    for the worker to process it.
    :param instance_handler: SubscriptionInstanceHandlerStrategy/UserInstanceHandlerStrategy
    :param data: json
    '''
    try:
        users = instance_handler.fetch_instance(data)
        if data["persist"] == True:
            persist_data(users, data["message"], data["provider"], ttl=data["ttl"])
        else:
            push_in_provider_topic(users, data["message"], data["provider"])

        return "Success"

    except ConnectionRefusedError:
        return "Fail"


@app.task()
def consume_notification():
    '''
    - Pulls the request from the kafka topic.
    - fetches the relevent data required for the processing of notification
    - processes it based on the type of notification user/subscription
    :return: Nothing
    '''
    try:
        consumer = KafkaConsumer(
            'notification',
            auto_offset_reset='latest',
            enable_auto_commit=True,
            value_deserializer=lambda m: loads(m.decode('utf-8')),
            bootstrap_servers=settings.BOOTSTRAP_SERVERS_CONSUMER)

        subscription_url = f"http://{settings.BASE_DATA_SERVICE_URL}/api/v1/subscription/get-subscribed-users/"
        user_url = f"http://{settings.BASE_DATA_SERVICE_URL}/api/v1/users/get-user-details/"

        subscription_instance_handler = SubscriptionInstanceHandlerStrategy(subscription_url)
        user_instance_handler = UserInstanceHandlerStrategy(user_url)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = []

            for data in consumer:
                data = data.value
                if data["type"] == "subscription":
                    futures.append(executor.submit(fetch_user_objects, instance_handler=subscription_instance_handler, data=data))
                else:
                    futures.append(executor.submit(fetch_user_objects, instance_handler=user_instance_handler, data=data))
            for future in concurrent.futures.as_completed(futures):
                print(future.result())

    except SoftTimeLimitExceeded:
        print("Restarting...")



consume_notification.delay()
