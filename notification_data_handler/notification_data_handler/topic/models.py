from django.conf import settings
from django.db import models

# Create your models here.
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from notification_data_handler.core.behaviour import StatusMixin


class Topic(TimeStampedModel, StatusMixin):
    name = models.CharField(_("topic name"), max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name


class Subscription(TimeStampedModel, StatusMixin):
    name = models.CharField(_("Subscription Name"), max_length=255, null=False, blank=False)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True)
    topic = models.OneToOneField("Topic", on_delete=models.CASCADE, null=False, blank=False, related_name="topic_subscription")

    def __str__(self):
        return self.name
