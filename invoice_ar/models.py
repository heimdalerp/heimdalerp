from django.db import models
from django.utils.translation import ugettext_lazy as _

from invoice.models import Client, CompanyInvoice


class ClientAR(models.Model):
    """
    This class extends the Client class defined in 'invoice'.
    It adds basics fields required by law in Argentina.
    """
    client = models.OneToOneField(Client)
    dni = models.CharField(
        _('DNI'),
        max_length=10,
        default="",
        blank=True,
        unique=True,
        help_text=_('Documento Nacional de Identidad means National '
                    'Identity Document. Everyone in Argentina has one. '
                    )
    )
    cuit = models.CharField(
        _('CUIT'),
        max_length=14,
        default="",
        blank=True,
        unique=True,
        help_text=_("Clave Única de Identificación Tributaria means "
                    "Unique Code of Tributary Identification. Everybody "
                    "who isn't an employee under somebody's payroll has "
                    "one."
                    )
    )
    cuil = models.CharField(
        _('CUIL'),
        max_length=14,
        default="",
        blank=True,
        unique=True,
        help_text=_("Clave Única de Identificación Laboral means "
                    "Unique Code of Labor Identification. Everybody "
                    "who is an employee under somebody's payroll has "
                    "one."
                    )
    )

    def __str__(self):
        return self.client

    class Meta:
        verbose_name = _('client')
        verbose_name_plural = _('clients')
        default_permissions = ('view', 'add', 'change', 'delete')


class CompanyInvoiceAR(models.Model):
    """
    This class extends the Company class defined in 'invoice'.
    It adds basics fields required by law in Argentina.
    """
    company = models.OneToOneField(CompanyInvoice)
    cuit = models.CharField(
        _('CUIT'),
        max_length=14,
        default="",
        blank=True,
        unique=True,
        help_text=_("Clave Única de Identificación Tributaria means "
                    "Unique Code of Tributary Identification. Everybody "
                    "who isn't an employee under somebody's payroll has "
                    "one. Even companies, NGOs, Fundations, etc."
                    )
    )
    iibb = models.CharField(
        _('IIBB'),
        max_length=15,
        default="",
        blank=True,
        help_text=_("Ingresos Brutos means Brute Income. It is a unique "
                    "code given by fiscal regulators of provinces'."
                    )
    )

    def __str__(self):
        return self.company

    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('companies')
        default_permissions = ('view', 'add', 'change', 'delete')
