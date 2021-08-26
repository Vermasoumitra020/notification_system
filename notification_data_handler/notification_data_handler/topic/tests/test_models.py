import pytest

from notification_data_handler.topic.models import Topic, Subscription
from notification_data_handler.users.models import User
pytestmark = pytest.mark.django_db


def test_topic_create():
    data = {"name" : "phone"}
    instance = Topic.objects.create(**data)
    assert instance.name == "phone"

def test_subscription_create():
    user_data = {"username": "user123", "email": "user123@mail.com", "password": "123456@"}
    user_instance = User.objects.create(**user_data)
    topic_data = {"name": "phone"}
    topic_instance = Topic.objects.create(**topic_data)

    instance = Subscription.objects.create(topic=topic_instance, name="sale")
    instance.user.set([user_instance.id])
    assert instance.name == "sale"
    assert instance.user.all()[0].id == user_instance.id
    assert instance.topic.id == topic_instance.id
