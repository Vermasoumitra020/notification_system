import pytest
from django.urls import resolve, reverse
from notification_data_handler.topic.models import Subscription, Topic

pytestmark = pytest.mark.django_db


@pytest.fixture()
def subscription():
    ti = Topic.objects.create(name="Fake name")
    return Subscription.objects.create(name="subs name", topic=ti)

def test_get_subsciption_details(subscription: Subscription):
    assert reverse("subscription:subscribed-user",
                   kwargs={"id": subscription.id}) == f"/api/v1/subscription/get-subscribed-users/{subscription.id}/"


def test_create_subscription():
    assert reverse("subscription:create-subscribed-user") == "/api/v1/subscription/create-subscription/"
    assert resolve("/api/v1/subscription/create-subscription/").view_name == "subscription:create-subscribed-user"


def test_update_subscription():
    assert reverse("subscription:update-subscribed-user") == "/api/v1/subscription/update-subscription/"
    assert resolve("/api/v1/subscription/update-subscription/").view_name == "subscription:update-subscribed-user"


def test_list_subscription():
    assert reverse("subscription:list-subscription") == "/api/v1/subscription/list-subscription/"
    assert resolve("/api/v1/subscription/list-subscription/").view_name == "subscription:list-subscription"


def test_delete_subscription(subscription:Subscription):
    assert reverse(f"subscription:delete-subscription", kwargs={"id": subscription.id}) == f"/api/v1/subscription/remove-subscription/{subscription.id}/"
