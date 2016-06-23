from django.db import models
from django.utils.translation import ugettext_lazy as _


class AlternativeName(models.Model):

    language_code = models.CharField(
        _('language code'),
        max_length=2,
        default='en'
    )
    name = models.CharField(
        _('name'),
        max_length=150
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('alternative name')
        verbose_name_plural = _('alternative names')
        default_permissions = ('view', 'add', 'change', 'delete')


class Country(models.Model):

    codename = models.CharField(
        _('codename'),
        max_length=2,
        unique=True,
        db_index=True
    )
    default_name = models.CharField(
        _('default name'),
        max_length=150
    )
    alternative_names = models.ManyToManyField(
        AlternativeName,
        verbose_name=_('alternative names'),
        related_name='+',
        related_query_name='+',
        blank=True
    )

    def __str__(self):
        return self.default_name

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')
        default_permissions = ('view', 'add', 'change', 'delete')


class Region(models.Model):

    country = models.ForeignKey(
        Country,
        verbose_name=_('country'),
        related_name='regions',
        related_query_name='region',
        on_delete=models.PROTECT,
        db_index=True
    )
    codename = models.CharField(
        _('codename'),
        max_length=4,
        default="",
        blank=True
    )
    default_name = models.CharField(
        _('default name'),
        max_length=150
    )
    alternative_names = models.ManyToManyField(
        AlternativeName,
        verbose_name=_('alternative names'),
        related_name='+',
        related_query_name='+',
        blank=True
    )

    def __str__(self):
        return self.default_name

    class Meta:
        verbose_name = _('region')
        verbose_name_plural = _('regions')
        default_permissions = ('view', 'add', 'change', 'delete')


class Locality(models.Model):

    region = models.ForeignKey(
        Region,
        related_name='localities',
        related_query_name='locality',
        verbose_name=_('region'),
        on_delete=models.PROTECT,
        db_index=True
    )
    default_name = models.CharField(
        _('default name'),
        max_length=150
    )
    alternative_names = models.ManyToManyField(
        AlternativeName,
        verbose_name=_('alternative names'),
        related_name='+',
        related_query_name='+',
        blank=True
    )

    def __str__(self):
        return self.default_name

    class Meta:
        verbose_name = _('locality')
        verbose_name_plural = _('localities')
        default_permissions = ('view', 'add', 'change', 'delete')
