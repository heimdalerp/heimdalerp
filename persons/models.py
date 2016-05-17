from cities_light.models import City, Country
from django.db import models
from django.utils.translation import ugettext_lazy as _

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

GENRE_TYPE_MALE = 'M'
GENRE_TYPE_FEMALE = 'F'
GENRE_TYPES = (
    (GENRE_TYPE_MALE, _('Male')),
    (GENRE_TYPE_FEMALE, _('Female'))
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
    """
    Employees and clients may have more than one email address.
    When in doubt, the official should always be the one in
    'django.contrib.auth.models.User.email'.
    """
    email = models.EmailField(
        _("email address")
    )
    description = models.CharField(
        _("description"),
        max_length=50,
        default="",
        blank=True
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("extra email address")
        verbose_name_plural = _("extra email addresses")
        default_permissions = ('view', 'add', 'change', 'delete')


class PhysicalAddress(models.Model):
    """
    Physical address are of high importance due to impositive regulations.
    """
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
        default=""
    )
    apartment_number = models.CharField(
        _("apartment number"),
        max_length=6,
        default=""
    )
    city = models.ForeignKey(
        City,
        related_name='physical_addresses',
        related_query_name='physical_address',
        verbose_name=_('city')
    )
    postal_code = models.CharField(
        _("postal code"),
        max_length=20
    )

    class Meta:
        verbose_name = _("physical address")
        verbose_name_plural = _("physical addresses")
        default_permissions = ('view', 'add', 'change', 'delete')


class PersonProfile(models.Model):
    """
    This is an abstract class where Employee and Client inherit their
    main attributes.
    """
    birth_date = models.DateField(
        _("birth date"),
        blank=True,
        null=True
    )
    born_in = models.ForeignKey(
        Country,
        verbose_name=_('born in'),
        blank=True,
        null=True
    )
    phone_numbers = models.ManyToManyField(
        PhoneNumber,
        blank=True,
        verbose_name=_('phone numbers')
    )
    extra_emails = models.ManyToManyField(
        ExtraEmailAddress,
        blank=True,
        verbose_name=_('extra email addresses')
    )

    class Meta:
        abstract = True


class Company(models.Model):
    """
    The companies using HeimdalERP.
    """
    name = models.CharField(
        _('name'),
        max_length=150,
        unique=True
    )
    initiated_activities = models.DateField(
        _('initiated activities'),
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('companies')
        default_permissions = ('view', 'add', 'change', 'delete')
