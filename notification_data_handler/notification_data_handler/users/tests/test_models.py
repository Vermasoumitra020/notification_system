import pytest

from notification_data_handler.users.models import User

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/api/v1/users/{user.username}/"
