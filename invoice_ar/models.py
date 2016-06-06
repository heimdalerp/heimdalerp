from django.db import models
from django.utils.translation import ugettext_lazy as _

from invoice.models import (CompanyInvoice,
                            ContactInvoice,
                            Invoice,
                            VAT)
from persons.models import PhysicalAddress

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
        verbose_name=_('contact'),
        primary_key=True
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
        return self.invoice_contact.contact_contact.name

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
        verbose_name=_('company'),
        primary_key=True
    )
    cuit = models.CharField(
        _('CUIT'),
        max_length=14,
        default="",
        blank=True,
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
        return self.invoice_company.persons_company.name

    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('companies')
        default_permissions = ('view', 'add', 'change', 'delete')


POINTOFSALE_TYPE_CONTROLADORFISCAL = 'C'
POINTOFSALE_TYPE_FACTUWEB = 'F'
POINTOFSALE_TYPE_WEBSERVICE = 'W'
POINTOFSALE_TYPE_ENLINEA = 'L'
POINTOFSALE_TYPES = (
    (POINTOFSALE_TYPE_CONTROLADORFISCAL, _('Fiscal Controller')),
    (POINTOFSALE_TYPE_FACTUWEB, _('Pre-printed')),
    (POINTOFSALE_TYPE_WEBSERVICE, _('Webservice')),
    (POINTOFSALE_TYPE_ENLINEA, _('Online')),
)


class PointOfSale(models.Model):
    """
    AFIP requires the following attributes related to a previously 
    registered in their website point of sale.
    """
    def _limit_fiscal_address(self):
        return {'company': self.invoicear_company.invoice_company}

    invoicear_company = models.ForeignKey(
        CompanyInvoiceAR,
        verbose_name=_('company'),
        related_name='point_of_sales',
        related_query_name='point_of_sale'
    )
    afip_id = models.PositiveSmallIntegerField(
        _('AFIP id')
    )
    point_of_sale_type = models.CharField(
        _('point of sale type'),
        max_length=1,
        choices=POINTOFSALE_TYPES,
        default=POINTOFSALE_TYPE_WEBSERVICE
    )
    fiscal_address = models.ForeignKey(
        PhysicalAddress,
        verbose_name=_('fiscal address'),
        related_name='point_of_sales',
        related_query_name='point_of_sale',
        on_delete=models.PROTECT,
        limit_choices_to=_limit_fiscal_address
    )
    is_inactive = models.BooleanField(
        _('is inactive'),
        default=False
    )

    def __str__(self):
        return 

    class Meta:
        unique_together = ('invoicear_company', 'afip_id')
        verbose_name = _('point of sale')
        verbose_name_plural = _('point of sales')
        default_permissions = ('view', 'add', 'change', 'delete')


class InvoiceType(models.Model):
    """
    AFIP's defined invoice types.
    """
    name = models.CharField(
        _('name'),
        max_length=10,
        unique=True
    )
    afip_code = models.SmallIntegerField(
        _('AFIP code'),
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('invoice type')
        verbose_name_plural = _('invoice types')
        default_permissions = ('view', 'add', 'change', 'delete')


SERVICE_TYPE_PRODUCT = 'P'
SERVICE_TYPE_SERVICE = 'S'
SERVICE_TYPE_PRODUCTANDSERVICE = 'PS'
SERVICE_TYPES = (
    (SERVICE_TYPE_PRODUCT, _('Product')),
    (SERVICE_TYPE_SERVICE, _('Service')),
    (SERVICE_TYPE_PRODUCTANDSERVICE, _('Product and service')),
)


class InvoiceAR(Invoice):
    """
    Invoice extension for Argentina.
    """
    point_of_sale = models.ForeignKey(
        PointOfSale,
        verbose_name=_('point of sale'),
        related_name='invoices_ar',
        related_query_name='invoice_ar',
        on_delete=models.PROTECT
    )
    due_date = models.DateField(
        _('due date')
    )
    service_start = models.DateField(
        _('service start')
    )
    service_type = models.CharField(
        _('service type'),
        max_length=2,
        choices=SERVICE_TYPES
    )
    vat_total = models.DecimalField(
        _('VAT total'),
        max_digits=15,
        decimal_places=2,
        default=0.00
    )
    vat_subtotals = models.ManyToManyField(
        'InvoiceARHasVATSubtotal',
        verbose_name=_('VAT subtotals'),
        related_name='+',
        related_query_name='invoicear'
    )

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = _('invoice')
        verbose_name_plural = _('invoice')
        default_permissions = ('view', 'add', 'change', 'delete')


class InvoiceARHasVATSubtotal(models.Model):
    """
    AFIP requires to compute each VAT's subtotal and store it.
    """
    vat = models.ForeignKey(
        VAT,
        verbose_name=_('VAT'),
        related_name='+',
        related_query_name='+'
    )
    subtotal = models.DecimalField(
        _('subtotal'),
        max_digits=15,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return str(self.subtotal)

    class Meta:
        verbose_name = _('VAT subtotal')
        verbose_name_plural = _('VAT subtotals')
        default_permissions = ('view', 'add', 'change', 'delete')   
