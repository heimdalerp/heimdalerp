from common.validators import date_is_past
from django.db import models
from django.utils.translation import gettext_lazy as _
from geo.models import Country, Locality

GENRE_TYPE_MALE = 'M'
GENRE_TYPE_FEMALE = 'F'
GENRE_TYPES = (
    (GENRE_TYPE_MALE, _('Male')),
    (GENRE_TYPE_FEMALE, _('Female'))
)


class PhysicalAddress(models.Model):
    """
    Physical address are of high importance due to impositive regulations.
    """
    street_address = models.CharField(
        _('street address'),
        max_length=150,
        default="",
        blank=True
    )
    floor_number = models.CharField(
        _('floor number'),
        max_length=4,
        default="",
        blank=True
    )
    apartment_number = models.CharField(
        _('apartment number'),
        max_length=6,
        default="",
        blank=True
    )
    locality = models.ForeignKey(
        Locality,
        related_name='physical_addresses',
        related_query_name='physical_address',
        verbose_name=_('locality'),
        on_delete=models.PROTECT,
        db_index=True,
        blank=True,
        null=True
    )
    postal_code = models.CharField(
        _('postal code'),
        max_length=20,
        default="",
        blank=True
    )

    def __str__(self):
        return self.street_address

    class Meta:
        verbose_name = _('physical address')
        verbose_name_plural = _('physical addresses')
        default_permissions = ('view', 'add', 'change', 'delete')


class Company(models.Model):
    """
    The companies using HeimdalERP.
    """
    fantasy_name = models.CharField(
        _('fantasy name'),
        max_length=150
    )
    slogan = models.CharField(
        _('slogan'),
        max_length=200,
        default="",
        blank=True
    )

    def __str__(self):
        return self.fantasy_name

    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('companies')
        default_permissions = ('view', 'add', 'change', 'delete')


class PersonProfile(models.Model):
    """
    This is an abstract class where Employee and Client inherit their
    main attributes.
    """
    persons_company = models.ForeignKey(
        Company,
        verbose_name=_('company'),
        related_name='+',
        related_query_name='+',
        db_index=True,
        on_delete=models.PROTECT
    )
    birth_date = models.DateField(
        _('birth date'),
        blank=True,
        null=True,
        validators=[date_is_past]
    )
    born_in = models.ForeignKey(
        Country,
        verbose_name=_('born in'),
        related_name='+',
        related_query_name='+',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    phone_numbers = models.CharField(
        _('phone numbers'),
        max_length=300,
        default="",
        blank=True
    )
    extra_emails = models.CharField(
        _('extra email addresses'),
        max_length=300,
        default="",
        blank=True,
    )
    home_address = models.ForeignKey(
        PhysicalAddress,
        on_delete=models.CASCADE,
        verbose_name=_('home address'),
        related_name='+',
        related_query_name='+',
        db_index=False,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True
