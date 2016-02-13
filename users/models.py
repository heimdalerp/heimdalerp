from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from django_countries.fields import CountryField


PHONENUMBER_TYPE_HOME = 'H'
PHONENUMBER_TYPE_WORK = 'W'
PHONENUMBER_TYPES = (
    (PHONENUMBER_TYPE_HOME, _("home")),
    (PHONENUMBER_TYPE_WORK, _("work")),
)

PHONENUMBER_TECHNOLOGYTYPE_LANDLINE = 'L'
PHONENUMBER_TECHNOLOGYTYPE_MOBILE = 'M'
PHONENUMBER_TECHNOLOGY_TYPES = (
    (PHONENUMBER_TECHNOLOGYTYPE_LANDLINE, _("landline phone")),
    (PHONENUMBER_TECHNOLOGYTYPE_MOBILE, _("mobile phone")),
)


class PhoneNumber(models.Model):
    user = models.ForeignKey(
        User,
        db_index=True
    )
    number = models.CharField(
    _("number"),
    max_length=30
    )
    phonenumber_type = models.CharField(
        _("phone number type"),
        max_length=1,
        choices=PHONENUMBER_TYPES,
        default=PHONENUMBER_TYPE_WORK
    )
    technology_type = models.CharField(
        _("technology type"),
        max_length=1,
        choices=PHONENUMBER_TECHNOLOGY_TYPES
        default=PHONENUMBER_TECHNOLOGYTYPE_MOBILE
    )
    created_by = models.ForeignKey(
        User,
        editable=False,
        related_name='+'
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )
    last_modified_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        editable=False,
        related_name='+'
    )
    last_modified_on = models.DateTimeField(
        auto_now=True,
        null=True
    )

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = _("phone number")
        verbose_name_plural = _("phone numbers")


class ExtraEmailAddress(models.Model):
    user = models.ForeignKey(
        User,
        db_index=True
    )
    email = models.EmailField(
        _("email address")
    )
    created_by = models.ForeignKey(
        User,
        editable=False,
        related_name='+'
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )
    last_modified_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        editable=False,
        related_name='+'
    )
    last_modified_on = models.DateTimeField(
        auto_now=True,
        null=True
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("extra email address")
        verbose_name_plural = _("extra email addresses")


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    birth_date = models.DateField(
        _("birth date"),
        blank=True,
        null=True
    )
    phone_numbers = models.ManyToManyField(
    PhoneNumber,
    blank=True,
    null=True
    )
    extra_emails = models.ManyToManyField(
    ExtraEmailAdress,
    blank=True,
    null=True
    )
    created_by = models.ForeignKey(
        User,
        editable=False,
        related_name='+'
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )
    last_modified_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        editable=False,
        related_name='+'
    )
    last_modified_on = models.DateTimeField(
        auto_now=True,
        null=True
    )

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")
