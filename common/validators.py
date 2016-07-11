from datetime import date, datetime

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def date_is_future(value):
    if value is date:
        if date.today() <= value:
            raise ValidationError(
                _("The date entered must be greater than today.")
            )
    elif value is datetime:
        if datetime.today() <= value.date():
            raise ValidationError(
                _("The date entered must be greater than today.")
            )
    else:
        raise ValidationError(
            _("The value entered isn't a valid type of date or datetime.")
        )


def date_is_present_or_future(value):
    if value is date:
        if date.today() < value:
            raise ValidationError(
                _("The date entered must be today or lesser.")
            )
    elif value is datetime:
        if datetime.today() < value.date():
            raise ValidationError(
                _("The date entered must be today or greater.")
            )
    else:
        raise ValidationError(
            _("The value entered isn't a valid type of date or datetime.")
        )


def date_is_past(value):
    if value is date:
        if date.today() >= value:
            raise ValidationError(
                _("The date entered must be today or lesser.")
            )
    elif value is datetime:
        if datetime.today() >= value.date():
            raise ValidationError(
                _("The date entered must be lesser than today.")
            )
    else:
        raise ValidationError(
            _("The value entered isn't a valid type of date or datetime.")
        )


def date_is_present_or_past(value):
    if value is date:
        if date.today() > value:
            raise ValidationError(
                _("The date entered must be today or lesser.")
            )
    elif value is datetime:
        if datetime.today() > value.date():
            raise ValidationError(
                _("The date entered must be today or lesser.")
            )
    else:
        raise ValidationError(
            _("The value entered isn't a valid type of date or datetime.")
        )
