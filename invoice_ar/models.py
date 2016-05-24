from django.db import models
from django.utils.translation import ugettext_lazy as _

from invoice.models import CompanyInvoice, ContactInvoice

ID_TYPE_DNI = 'D'
ID_TYPE_CUIT = 'T'
ID_TYPE_CUIL = 'L'
ID_TYPES = (
    (ID_TYPE_DNI, _('DNI')),
    (ID_TYPE_CUIT, _('CUIT')),
    (ID_TYPE_CUIL, _('CUIL')),
)


class ContactInvoiceAR(models.Model):
    """
    This class extends the Contact class defined in 'invoice'.
    It adds basics fields required by law in Argentina.
    """
    invoice_contact = models.OneToOneField(
        ContactInvoice,
        verbose_name=_('contact')
    )
    id_type = models.CharField(
        _('id type'),
        max_length=1,
        choices=ID_TYPES,
        blank=True,
        null=True
    )
    id_number = models.CharField(
        _('id number'),
        max_length=14,
        default="",
        blank=True
    )

    def __str__(self):
        return self.contact

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')
        default_permissions = ('view', 'add', 'change', 'delete')


class CompanyInvoiceAR(models.Model):
    """
    This class extends the Company class defined in 'invoice'.
    It adds basics fields required by law in Argentina.
    """
    invoice_company = models.OneToOneField(
        CompanyInvoice,
        verbose_name=_('company')
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
