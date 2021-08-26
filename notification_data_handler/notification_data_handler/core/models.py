from __future__ import unicode_literals, absolute_import

from datetime import timedelta

# Core Django imports
from django.conf import settings
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from six import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from .utils import create_slug
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import Group
# Third-party app imports
from model_utils.models import TimeStampedModel

# Imports from segregator apps
from .behaviour import (
    SlugMixin,
    StatusMixin,
    UserStampedMixin,
    GenericForeignKeyMixin,
    AddressMixin,
    MobileMixin,
)

from .utils import truncate_text
from .validators import validator_ascii


class Country(SlugMixin):
    name = models.CharField(
        _("name"), max_length=100, blank=False, null=False, validators=[validator_ascii],
        help_text="The length of this field can't be longer than 100",
    )

    def __str__(self):
        return str(self.name)


@python_2_unicode_compatible
class State(SlugMixin):
    name = models.CharField(
        _("name"), max_length=100, blank=False, null=False, validators=[validator_ascii],
        help_text="The length of this field can't be longer than 100"
    )
    TYPE_CHOICES = (
        ("E", "East"),
        ("W", "West"),
        ("N", "North"),
        ("S", "South"),
        ("C", "Central"),
    )
    region = models.CharField(max_length=255, choices=TYPE_CHOICES, blank=True, null=True)
    country = models.ForeignKey("core.Country", models.SET_NULL, blank=False, null=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class City(StatusMixin, SlugMixin):
    name = models.CharField(
        _("name"), max_length=60, blank=False, null=False, validators=[validator_ascii],
        help_text="The length of this field can't be longer than 60"
    )
    state = models.ForeignKey("core.State", models.SET_NULL, blank=False, null=True)
    synonym = models.CharField(
        _("synonym name"),
        max_length=255,
        blank=True,
        null=True,
        validators=[validator_ascii],
    )
    is_targeted_city = models.BooleanField(default=False, blank=True)
    canonical_slug = models.CharField(
        _("Canonical Slug"),
        max_length=255,
        blank=True,
        null=True,
        validators=[validator_ascii],
    )

    def __str__(self):
        if self.name:
            return str(self.name)
        return str(self.id)

    class Meta:
        verbose_name_plural = "Cities"

    def save(self, *args, **kwargs):
        cache.delete("cities")

        if not self.canonical_slug:
            self.canonical_slug = create_slug(self)
        if self.canonical_slug:
            self.canonical_slug = self.canonical_slug.replace(" ", "")

        super(City, self).save(*args, **kwargs)


@python_2_unicode_compatible
class District(StatusMixin, SlugMixin):
    name = models.CharField(
        _("name"), max_length=60, blank=False, null=False, validators=[validator_ascii],
        help_text="The length of this field can't be longer than 60"
    )
    state = models.ForeignKey("core.State", models.SET_NULL, blank=False, null=True)

    def __str__(self):
        if self.name:
            return str(self.name)
        return str(self.id)

    class Meta:
        verbose_name = "District"


@python_2_unicode_compatible
class PINCode(SlugMixin):
    value = models.CharField(
        _("PIN Code"), max_length=50, blank=False, null=False, validators=[validator_ascii],
        help_text="The number of char can't be  more than 50")

    def __str__(self):
        if self.value:
            return str(self.value)
        return self.id

    class Meta:
        verbose_name = "Pin Code"


@python_2_unicode_compatible
class File(TimeStampedModel):
    name = models.CharField(
        _("name"), max_length=255, blank=False, null=False, validators=[validator_ascii]
    )
    file = models.FileField(_("file"), default=True, null=True)
    description = models.TextField(
        _("description"), blank=True, validators=[validator_ascii]
    )

    def __str__(self):
        return str(self.name)


@python_2_unicode_compatible
class Comment(StatusMixin, TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True
    )
    content = models.TextField(_("content"), blank=True, validators=[validator_ascii])

    def __str__(self):
        return truncate_text(self.content, limit=50)


@python_2_unicode_compatible
class Mobile(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="mobile_user",
    )
    regex = RegexValidator(regex=r"^[1-9]\d{9}$", message="Invalid Mobile Number")

    country_code_regex = RegexValidator(
        regex=r"^\+[0-9]{1,4}", message="Invalid Country Code"
    )
    mobile = models.CharField(
        _("mobile number"),
        validators=[regex],
        blank=True,
        null=True,
        max_length=10,
        unique=True,
        help_text="Enter a valid 10 digit mobile number.",
    )
    verified = models.BooleanField(verbose_name=_("verified"), default=False)
    country_code = models.CharField(
        _("Country Code"),
        validators=[country_code_regex],
        blank=True,
        null=True,
        max_length=5,
    )

    def __str__(self):
        return str(self.mobile)






@python_2_unicode_compatible
class Branch(StatusMixin, SlugMixin, AddressMixin, TimeStampedModel, MobileMixin):
    name = models.CharField(
        _("Branch Name"),
        max_length=30,
        help_text="The length of this field can't be longer than 30",
        blank=False,
        null=False,
        validators=[validator_ascii],
    )
    branch_id = models.CharField(
        _("Branch ID"),
        max_length=20,
        blank=False,
        null=False,
        validators=[validator_ascii],
        help_text="The length of this field can't be longer than 20"
    )
    branch_head = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="branch_head",
    )
    email = models.EmailField(_("email address"), blank=True, null=True)
    region = models.ForeignKey("Region", models.SET_NULL, blank=True, null=True, related_name="region_name")

    def __str__(self):
        if self.name:
            return str(self.name)
        return str(self.id)


@python_2_unicode_compatible
class Region(models.Model):
    name = models.CharField(
        _("Region Name"),
        max_length=100,
        help_text="The length of this field can't be longer than 100",
        blank=False,
        null=False,
        validators=[validator_ascii],
    )

    def __str__(self):
        if self.name:
            return str(self.name)
        return str(self.id)








