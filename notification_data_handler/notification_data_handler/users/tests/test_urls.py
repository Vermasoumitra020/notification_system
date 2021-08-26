import pytest
from django.urls import resolve, reverse

from notification_data_handler.users.models import User

pytestmark = pytest.mark.django_db


def test_detail(user: User):
    assert (
        reverse("users:detail", kwargs={"username": user.username})
        == f"/api/v1/users/{user.username}/"
    )
    assert resolve(f"/api/v1/users/{user.username}/").view_name == "users:detail"


def test_update():
    assert reverse("users:update") == "/api/v1/users/~update/"
    assert resolve("/api/v1/users/~update/").view_name == "users:update"


def test_redirect():
    assert reverse("users:redirect") == "/api/v1/users/~redirect/"
    assert resolve("/api/v1/users/~redirect/").view_name == "users:redirect"
