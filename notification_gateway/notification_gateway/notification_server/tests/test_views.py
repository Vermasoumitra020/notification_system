import pytest
from rest_framework import status
from rest_framework.response import Response

from notification_gateway.notification_server.views import SendMessageToQueue
from django.test import RequestFactory


@pytest.fixture()
def send_message_to_queue():
    return SendMessageToQueue()


class TestSendMessageToQueue:

    def test_invalid_field_post(self, send_message_to_queue, rf: RequestFactory):
        view = send_message_to_queue

        data = {
            "ids": [1],
            "type": "user",
            "provider": "mail",
            "message": {
                "title": "nothing",
                "description": "nothing"
            },
            "persist": True
        }

        true_response = Response(status=status.HTTP_400_BAD_REQUEST)

        request = rf.post("/fake-url/")
        request.data = data
        response = view.post(request)

        assert response.status_code == true_response.status_code

    def test_valid_post(self, send_message_to_queue, rf: RequestFactory):
        view = send_message_to_queue

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

        true_response = Response(status=status.HTTP_200_OK)

        request = rf.post("/fake-url/")
        request.data = data
        response = view.post(request)

        assert response.status_code == true_response.status_code

