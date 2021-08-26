from django.urls import resolve, reverse


def test_send_notification():
    assert reverse("notification_server:send-notif") == "/api/v1/notification-server/notify/"
    assert resolve("/api/v1/notification-server/notify/").view_name == "notification_server:send-notif"
