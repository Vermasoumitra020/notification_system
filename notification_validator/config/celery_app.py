import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("notification_validator")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    'pull-message-from-queue': {
        'task': 'notification_validator.notification_consumer.views.consume_notification',
        'schedule': crontab(hour=0, minute=1),
    },
    'schedule-message-from-database': {
        'task': 'notification_validator.notifications.scheduler.schedule_message',
        'schedule': crontab(hour=0, minute=1),
    },
}
