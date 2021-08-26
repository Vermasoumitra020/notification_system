from django.db import models

# Create your models here.
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _


class Notification(TimeStampedModel):
    is_expired = models.BooleanField(_("Expiration Time"), default=False)
    time_to_live = models.PositiveIntegerField(_("time to live"), null=True, blank=True)
    message = models.JSONField(_("message"), null=True, blank=True)
    provider = models.CharField(_("Provider"), max_length=255, null=True, blank=True)
    PRIORITY = (("High", ("High")),
                ("Medium", "Medium"),
                ("Low", "Low"))
    priority = models.CharField(_("Priority"), choices=PRIORITY, max_length=255, default="Medium")
    users = models.JSONField(_("Users list"), null=True, blank=True)



