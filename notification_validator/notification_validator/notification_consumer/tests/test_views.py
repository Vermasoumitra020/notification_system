import pytest
from django.conf import settings

from notification_validator.notification_consumer.handler.instance_handler import SubscriptionInstanceHandlerStrategy, \
    UserInstanceHandlerStrategy
from notification_validator.notification_consumer.views import fetch_user_objects

pytestmark = pytest.mark.django_db

def test_fetch_subscription_objects():
    subscription_url = f"http://{settings.BASE_DATA_SERVICE_URL}/api/v1/subscription/get-subscribed-users/"

    instance_handler = SubscriptionInstanceHandlerStrategy(subscription_url)
    data = {
            "ids": [1],
            "type": "subscription",
            "provider": "mail",
            "message": {
                "title": "nothing",
                "description": "nothing"
            },
            "persist": True,
            "ttl": 7
        }
    res = fetch_user_objects(instance_handler, data)

    assert res == "Success"


def test_fetch_user_objects():
    user_url = f"http://{settings.BASE_DATA_SERVICE_URL}/api/v1/users/get-user-details/"

    instance_handler = UserInstanceHandlerStrategy(user_url)
    data = {
            "ids": [1],
            "type": "subscription",
            "provider": "mail",
            "message": {
                "title": "nothing",
                "description": "nothing"
            },
            "persist": True,
            "ttl": 7
        }
    res = fetch_user_objects(instance_handler, data)

    assert res == "Success"


def test_subscription_handler():
    subscription_url = f"http://{settings.BASE_DATA_SERVICE_URL}/api/v1/subscription/get-subscribed-users/"


    data = {
        "ids": [1],
        "type": "user",
        "provider": "mail",
        "message": {
            "title": "nothing",
            "description": "nothing"
        },
        "persist": True,
        "ttl": 7
    }
    instance = SubscriptionInstanceHandlerStrategy(subscription_url)
    res = instance.fetch_instance(data)

    assert len(res) > 0


def test_user_handler():
    user_url = f"http://{settings.BASE_DATA_SERVICE_URL}/api/v1/users/get-user-details/"

    data = {
        "ids": [1],
        "type": "user",
        "provider": "mail",
        "message": {
            "title": "nothing",
            "description": "nothing"
        },
        "persist": True,
        "ttl": 7
    }
    instance = UserInstanceHandlerStrategy(user_url)
    res = instance.fetch_instance(data)

    assert len(res) > 0
