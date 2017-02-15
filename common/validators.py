import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def date_is_future(value):
    if isinstance(value, datetime.date):
        if value <= datetime.date.today():
            raise ValidationError(
                _("The date entered must be greater than today.")
            )
    elif isinstance(value, datetime.datetime):
        if value.date() <= datetime.today():
            raise ValidationError(
                _("The date entered must be greater than today.")
            )
    else:
        raise ValidationError(
            _("The value entered isn't a valid type of date or datetime.")
        )


def date_is_present_or_future(value):
    if isinstance(value, datetime.date):
        if value < datetime.date.today():
            raise ValidationError(
                _("The date entered must be today or lesser.")
            )
    elif isinstance(value, datetime.datetime):
        if value.date() < datetime.datetime.today():
            raise ValidationError(
                _("The date entered must be today or greater.")
            )
    else:
        raise ValidationError(
            _("The value entered isn't a valid type of date or datetime.")
        )


def date_is_past(value):
    if isinstance(value, datetime.date):
        if value >= datetime.date.today():
            raise ValidationError(
                _("The date entered must be today or lesser.")
            )
    elif isinstance(value, datetime.datetime):
        if value.date() >= datetime.datetime.today():
            raise ValidationError(
                _("The date entered must be lesser than today.")
            )
    else:
        raise ValidationError(
            _("The value entered isn't a valid type of date or datetime.")
        )


def date_is_present_or_past(value):
    if isinstance(value, datetime.date):
        if value > datetime.date.today():
            raise ValidationError(
                _("The date entered must be today or lesser.")
            )
    elif isinstance(value, datetime.datetime):
        if value.date() > datetime.datetime.today():
            raise ValidationError(
                _("The date entered must be today or lesser.")
            )
    else:
        raise ValidationError(
            _("The value entered isn't a valid type of date or datetime.")
        )
