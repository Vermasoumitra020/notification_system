# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.validators import RegexValidator

validator_ascii = RegexValidator(
    regex=r"^[\x00-\x7F]*$", message="Only ASCII characters allowed"
)


validator_pan_no = RegexValidator(
    regex=r"^[A-Z]{5}\d{4}[A-Z]$", message="Please provide a valid pan number"
)
