from django.db import models
from django.utils.translation import ugettext_lazy as _

from cities_light.models import City


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

PHYSICALADDRESS_TYPE_FISCAL = 'F'
PHYSICALADDRESS_TYPE_HOME = 'H'
PHYSICALADDRESS_TYPES = (
    (PHYSICALADDRESS_TYPE_FISCAL, _("fiscal")),
    (PHYSICALADDRESS_TYPE_HOME, _("home")),
)

class PhoneNumber(models.Model):
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
        choices=PHONENUMBER_TECHNOLOGY_TYPES,
        default=PHONENUMBER_TECHNOLOGYTYPE_MOBILE
    )

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = _("phone number")
        verbose_name_plural = _("phone numbers")
        default_permissions = ('view', 'add', 'change', 'delete')


class ExtraEmailAddress(models.Model):
    email = models.EmailField(
        _("email address")
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("extra email address")
        verbose_name_plural = _("extra email addresses")
        default_permissions = ('view', 'add', 'change', 'delete')


class PhysicalAddress(models.Model):
    address_type = models.CharField(
        _("address type"),
        max_length=1,
        choices=PHYSICALADDRESS_TYPES,
        default=PHYSICALADDRESS_TYPE_FISCAL
    )
    street_name = models.CharField(
        _("street name"),
        max_length=150
    )
    street_number = models.CharField(
        _("street number"),
        max_length=10
    )
    floor_number = models.CharField(
        _("floor number"),
        max_length=4,
        blank=True,
        null=True
    )
    apartment_number = models.CharField(
        _("apartment number"),
        max_length=6,
        blank=True,
        null=True
    )
    city = models.ForeignKey(City)
    postal_code = models.CharField(
        _("postal code"),
        max_length=20
    )

    class Meta:
        verbose_name = _("extra email address")
        verbose_name_plural = _("extra email addresses")
        default_permissions = ('view', 'add', 'change', 'delete')
    

class PersonProfile(models.Model):
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
        ExtraEmailAddress,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True
