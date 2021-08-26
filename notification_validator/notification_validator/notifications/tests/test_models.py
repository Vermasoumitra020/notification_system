import pytest

from notification_validator.notifications.models import Notification

pytestmark = pytest.mark.django_db

def test_create_notification():
    data = {"users": [
            {
                "id": 1,
                "name": "Soumitra Soni",
                "first_name": "",
                "last_name": "",
                "email": "sonisoumitra@gmail.com",
                "phone": "",
                "device": [
                    {
                        "device_type": "Mobile",
                        "device_id": "678953YUB4532"
                    }
                ]
            }
        ], "provider": "mail", "message": {"title": "nothing", "description": "nothing"}, "time_to_live": 7}
    notification = Notification.objects.create(**data)
    assert notification.provider == "mail"
    assert notification.time_to_live == 7
