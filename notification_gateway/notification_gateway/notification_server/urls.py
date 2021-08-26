from django.urls import path
from .views import *

app_name = "notification_server"
urlpatterns=[
    path("notify/", SendMessageToQueue.as_view(), name="send-notif"),
]
