from django.db import models
from django.utils.translation import ugettext_lazy as _

from invoice.models import VAT, CompanyInvoice, ContactInvoice, Invoice
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
        verbose_name=_('company')
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
        help_text=_("Ingresos Brutos means gross revenue. It is a unique "
                    "code given by fiscal regulators of provinces'."
                    )
    )

    def __str__(self):
        return str(self.invoice_company)

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
        on_delete=models.PROTECT
    )
    is_inactive = models.BooleanField(
        _('is inactive'),
        default=False
    )

    def __str__(self):
        return str(self.afip_id) + ' @ ' + str(self.invoicear_company)

    class Meta:
        unique_together = ('invoicear_company', 'afip_id')
        verbose_name = _('point of sale')
        verbose_name_plural = _('point of sales')
        default_permissions = ('view', 'add', 'change', 'delete')


class ConceptType(models.Model):
    """
    Required by AFIP for every invoice made.
    """
    name = models.CharField(
        _('name'),
        max_length=50,
        unique=True
    )
    code = models.SlugField(
        _('code'),
        max_length=15,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('concept type')
        verbose_name_plural = _('concept types')
        default_permissions = ('view', 'add', 'change', 'delete')


class InvoiceAR(Invoice):
    """
    Invoice extension for Argentina.
    """
    invoicear_company = models.ForeignKey(
        CompanyInvoiceAR,
        verbose_name=_('company AR'),
        related_name='invoices',
        related_query_name='invoice',
        on_delete=models.PROTECT,
        db_index=True
    )
    invoicear_contact = models.ForeignKey(
        ContactInvoiceAR,
        verbose_name=_('contact AR'),
        related_name='invoices',
        related_query_name='invoice',
        on_delete=models.PROTECT,
        db_index=True
    )
    point_of_sale = models.ForeignKey(
        PointOfSale,
        verbose_name=_('point of sale'),
        related_name='invoices_ar',
        related_query_name='invoice_ar',
        on_delete=models.PROTECT,
        db_index=True
    )
    due_date = models.DateField(
        _('due date')
    )
    service_start = models.DateField(
        _('service start'),
        blank=True,
        null=True
    )
    concept_type = models.ForeignKey(
        ConceptType,
        verbose_name=_('concept type'),
        related_name='invoices',
        related_query_name='invoice',
        on_delete=models.PROTECT,
        db_index=True
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
        related_query_name='invoicear',
        blank=True
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
        return str(self.vat) + ':' + str(self.subtotal)

    class Meta:
        verbose_name = _('VAT subtotal')
        verbose_name_plural = _('VAT subtotals')
        default_permissions = ('view', 'add', 'change', 'delete')
