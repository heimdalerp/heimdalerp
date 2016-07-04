from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def date_is_future(value):
    if datetime.today() <= value.date():
        raise ValidationError(
            _("The date entered must be greater than today.")
        )


def date_is_present_or_future(value):
    if datetime.today() < value.date():
        raise ValidationError(
            _("The date entered must be today or greater.")
        )


def date_is_past(value):
    if datetime.today() >= value.date():
        raise ValidationError(
            _("The date entered must be lesser than today.")
        )


def date_is_present_or_past(value):
    if datetime.today() > value.date():
        raise ValidationError(
            _("The date entered must be today or lesser.")
        )
