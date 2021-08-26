# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from ckeditor_uploader.fields import RichTextUploadingField
from model_utils.models import TimeStampedModel

from .managers import (
    StatusMixinManager,
    GenericForeignKeyMixinManager,
    PostMixinManager,
)
from .utils import  OverwriteStorage, create_slug
from .validators import validator_ascii


class StatusMixin(models.Model):
    is_active = models.BooleanField(_("active"), default=True, blank=False, null=False)
    is_deleted = models.BooleanField(
        _("deleted"), default=False, blank=False, null=False
    )

    objects = StatusMixinManager()

    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save()

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.save()

    def remove(self):
        if not self.is_deleted:
            self.is_deleted = True
            self.save()

    def has_changed(self, field):
        model = self.__class__.__name__
        return getattr(self, field) != getattr(
            self, "_" + model + "__original_" + field
        )

    def save(self, *args, **kwargs):
        """
        Makes sure that the ``is_active`` is ``False`` when ``is_deleted`` is ``True``.
        """
        if self.is_deleted:
            self.is_active = False
        super(StatusMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class UserStampedMixin(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="created_%(class)s",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="updated_%(class)s",
    )

    class Meta:
        abstract = True


class MobileMixin(models.Model):
    regex = RegexValidator(regex=r"^[1-9]\d{9}$", message="Invalid Mobile Number")
    mobile = models.CharField(
        _("mobile number"),
        validators=[regex],
        blank=True,
        null=True,
        max_length=10,
        help_text="Enter a valid 10 digit mobile number.",
    )

    country_code_regex = RegexValidator(
        regex=r"^\+[0-9]{1,4}", message="Invalid Country Code"
    )
    country_code = models.CharField(
        _("Country Code"),
        validators=[country_code_regex],
        blank=True,
        null=True,
        max_length=5,
    )

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    slug = models.SlugField(blank=True, null=True, max_length=255)

    def save(self, *args, **kwargs):
        """
        slug  shouldn't have spaces
        """
        if not self.slug:
            self.slug = create_slug(self)
        if self.slug:
            self.slug = self.slug.replace(" ", "")
        super(SlugMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class GeoTagMixin(models.Model):
    lat = models.CharField(_("latitude"), blank=True, null=True, max_length=20)
    lng = models.CharField(_("longitude"), blank=True, null=True, max_length=20)

    class Meta:
        abstract = True


class IPAddressMixin(models.Model):
    ip_address = models.GenericIPAddressField(_("IP Address"), blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Auto saving the IP Address
        """
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(",")[-1].strip()
        else:
            ipaddress = self.request.META.get("REMOTE_ADDR")

        self.ip_address = ipaddress

        super(IPAddressMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class GenericForeignKeyMixin(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    objects = GenericForeignKeyMixinManager()

    class Meta:
        abstract = True


class ImageMixin(models.Model):
    image = models.ImageField(
        _("image"),  null=True, blank=True
    )
    image_alt = models.CharField(
        _("image alt"), max_length=100, blank=True, validators=[validator_ascii]
    )

    class Meta:
        abstract = True


class MetaTagMixin(models.Model):
    meta_title = models.TextField(
        _("Meta Title"), blank=True, null=True, validators=[validator_ascii]
    )
    meta_description = models.TextField(
        _("Meta Description"), blank=True, null=True, validators=[validator_ascii]
    )
    meta_keywords = models.TextField(
        _("Meta Keywords"), blank=True, null=True, validators=[validator_ascii]
    )

    class Meta:
        abstract = True


# COMPOUND MIXINS
#   ---------------------------------------------------------------------------------------------------------------


class AddressMixin(GeoTagMixin):
    house_no = models.TextField(
        _("Address Line 1"), max_length=100, blank=True, null=True, validators=[validator_ascii],
        help_text="The length of this field can't be longer than 100"
    )
    street = models.TextField(
        _("Address Line 2"), max_length=100, blank=True, null=True, validators=[validator_ascii],
        help_text="The length of this field can't be longer than 100"
    )
    locality = models.TextField(
        _("Locality"), blank=True, null=True, validators=[validator_ascii]
    )
    district = models.ForeignKey("core.District", models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey("core.City", models.SET_NULL, blank=True, null=True)
    pin_code = models.ForeignKey("core.PINCode", models.SET_NULL, blank=True, null=True)

    def get_address(self):
        address = ""
        if self.house_no:
            address += self.house_no
        if self.street:
            address += ", " + self.street
        if self.locality:
            address += ", " + self.locality
        if self.district:
            address += ", " + self.district.name
        if self.city and self.city.name:
            address += ", " + self.city.name
            if self.city.state and self.city.state.name:
                address += ", " + self.city.state.name
                if self.city.state.country and self.city.state.country.name:
                    address += ", " + self.city.state.country.name
        if self.pin_code:
            address += " - " + str(self.pin_code.value)

        if address == "":
            return None
        else:
            return "".join([i if ord(i) < 128 else " " for i in address])

    class Meta:
        abstract = True


class ProfileMixin(MobileMixin, AddressMixin):
    alternate_phone = models.CharField(
        max_length=50, blank=True, null=True, validators=[validator_ascii],
        help_text="The length of this field can't be longer than 50",
    )
    alternate_email = models.EmailField(
        max_length=80, blank=True, null=True, validators=[validator_ascii],
        help_text="The length of this field can't be longer than 80",
    )
    date_of_birth = models.DateField(blank=True, null=True)
    GENDER_CHOICES = (("M", "Male"), ("F", "Female"))
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True, default=None
    )

    class Meta:
        abstract = True






