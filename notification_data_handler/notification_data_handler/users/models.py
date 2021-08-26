from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from django.db import models
from notification_data_handler.core.behaviour import StatusMixin

# from django_mode


class User(AbstractUser):
    """Default user for notification_data_handler."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    phone = models.CharField(_("Phone number"), max_length=12, null=True, blank=True)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})




class UserDevice(TimeStampedModel, StatusMixin):
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=False, blank=False)
    device_type = models.CharField(_("Device Type"), max_length=255, null=True, blank=True)
    device_id = models.TextField(_("Device Unique ID"), null=False, blank=False)

    def __str__(self):
        return str(self.id)


