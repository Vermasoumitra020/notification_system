from kafka import KafkaProducer
from json import dumps
from notification_validator.notifications.models import Notification
from datetime import datetime, timedelta
from config.celery_app import app
from django.conf import settings

def is_valid(data):
    print(str(data["created"]))
    data_date = datetime.strptime(str(data["created"]).split(" ")[0], '%Y-%m-%d')
    end_date = data_date + timedelta(days=data["time_to_live"])

    if datetime.now().date() == end_date.date():
        return False
    return True


@app.task()
def schedule_message():
    queryset = Notification.objects.filter(is_expired = False).values()
    producer = KafkaProducer(
        value_serializer=lambda m: dumps(m).encode('utf-8'),
        bootstrap_servers=settings.BOOTSTRAP_SERVERS_PRODUCERS)

    for data in queryset:
        if is_valid(data):
            req = {"users": data["users"], "message": data["message"]}
            producer.send(data["provider"], value=req)


schedule_message.delay()
