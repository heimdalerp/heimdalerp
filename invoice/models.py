from django.db import models
from django.utils.translation import ugettext_lazy as _

from persons.models import PersonProfile


class FiscalPosition(models.Model):
    """
    A fiscal position is a classification given by a government to an
    individual or a company, which categorizes them into a tax-paying class.
    """
    name = models.CharField(
        _('name'),
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('fiscal position')
        verbose_name_plural = _('fiscal positions')
        default_permissions = ('view', 'add', 'change', 'delete')


class Company(models.Model):
    """
    You need to define at least one to start invoicing, but you can add
    as many as you need.
    """
    name = models.CharField(
        _('name'),
        max_length=150,
        unique=True
    )
    initiated_activies = models.DateField(
        _('initiated activies'),
        blank=True,
        null=True
    )
    fiscal_position = models.ForeignKey(
        FiscalPosition,
        verbose_name=_('fiscal position'),
        blank=True,
        null=True,
        help_text=_('Certain countries require a fiscal position for '
                    ' its taxpayers.')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('ethnicities')
        default_permissions = ('view', 'add', 'change', 'delete')


CLIENT_TYPE_COMPANY = 'C'
CLIENT_TYPE_INDIVIDUAL = 'I'
CLIENT_TYPES = (
    (CLIENT_TYPE_COMPANY, _('Company')),
    (CLIENT_TYPE_INDIVIDUAL, _('Individual')),
)

class Client(PersonProfile):
    """
    These are the clients (companies or individuals) which you'll invoice
    from your company.
    """
    name = models.CharField(
        _('name'),
        max_length=150,
        unique=True
    )
    client_type = models.CharField(
        _('client type'),
        max_length=1,
        choices=CLIENT_TYPES,
    )
    fiscal_position = models.ForeignKey(
        FiscalPosition,
        verbose_name=_('fiscal position'),
        blank=True,
        null=True,
        help_text=_('Certain countries require a fiscal position for '
                    ' its taxpayers.')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('client')
        verbose_name_plural = _('clients')
        default_permissions = ('view', 'add', 'change', 'delete')


class VAT(models.Model):
    """
    VAT is a type of tax to consumption. Every country has it.
    """
    name = models.CharField(
        _('name'),
        max_length=15,
        unique=True,
        help_text=_('i.e. 8%')
    )
    tax = models.FloatField(
        _('tax'),
        help_text=_('A value between 0.00 and 1.00')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('VAT')
        verbose_name_plural = _('VATs')
        default_permissions = ('view', 'add', 'change', 'delete')


class InvoiceProduct(models.Model):
    """
    A basic product. It could also be a service.
    See other modules like 'sales' for more advanced products.
    """
    company = models.ForeignKey(
        Company,
        verbose_name=_('company')
    )
    name = models.CharField(
        _('name'),
        max_length=150,
        help_text=_('It could also be a service.')
    )
    suggested_price = models.DecimalField(
        _('suggested price'),
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    vat = models.ForeignKey(
        VAT,
        verbose_name=_('VAT')
    )
 
    def __str__(self):
        return "%(product)s x %(quantity)s" % {
            'product': self.product,
            'quantity': self.quantity
        }

    class Meta:
        unique_together = (('company', 'name'),)
        index_together = [['company', 'name'],]
        verbose_name = _('product')
        verbose_name_plural = _('products')
        default_permissions = ('view', 'add', 'change', 'delete')


class InvoiceLine(models.Model):
    """
    An invoice of composed of lines or entries, which have a product,
    a price and a quantity.
    """
    product = models.ForeignKey(
        InvoiceProduct,
        verbose_name=_('product')
    )
    product_price_override = models.DecimalField(
        _('product price'),
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    product_vat_override = models.ForeignKey(
        VAT,
        verbose_name=_('VAT override'),
        blank=True,
        null=True
    )
    product_discount = models.FloatField(
        _('product discount'),
        default=0.00,
        blank=True,
        help_text=_('A number between 0.00 and 1.00')
    )
    quantity = models.PositiveIntegerField(
        _('quantity'),
        default=1
    )

    def __str__(self):
        return "%(product)s x %(quantity)s" % {
            'product': self.product,
            'quantity': self.quantity
        }

    class Meta:
        verbose_name = _('invoice line')
        verbose_name_plural = _('invoice lines')
        default_permissions = ('view', 'add', 'change', 'delete')
    

INVOICE_STATUSTYPE_DRAFT = 'D'
INVOICE_STATUSTYPE_SENT = 'S'
INVOICE_STATUSTYPE_PAID = 'P'
INVOICE_STATUSTYPE_CANCELED = 'C'
INVOICE_STATUS_TYPES = (
    (INVOICE_STATUSTYPE_DRAFT, _('Draft')),
    (INVOICE_STATUSTYPE_SENT, _('Sent')),
    (INVOICE_STATUSTYPE_PAID, _('Paid')),
    (INVOICE_STATUSTYPE_CANCELED, _('Canceled'))
)

class Invoice(models.Model):
    """
    The invoices themselves.
    """
    company = models.ForeignKey(
        Company,
        verbose_name=_('company'),
        db_index=True
    )
    clients = models.ManyToManyField(
        Client,
        related_name='clients',
        verbose_name=_('clients')
    )
    number = models.BigIntegerField(
        _('number')
    )
    invoice_lines = models.ManyToManyField(
        InvoiceLine,
        related_name='lines',
        verbose_name=_('lines')
    )
    invoice_date = models.DateField(
        _('date'),
        help_text=_('Not necessarily today.')
    )
    invoice_status = models.CharField(
        _('status'),
        max_length=1,
        choices=INVOICE_STATUS_TYPES,
        default=INVOICE_STATUSTYPE_DRAFT
    )
    notes = models.TextField(
        _('notes'),
        blank=True,
        default=""
    )

    def __str__(self):
        return "%(company)s : %(number)s" % {
            'company': self.company,
            'number': self.number
        }    

    class Meta:
        verbose_name = _('invoice')
        verbose_name_plural = _('invoices')
        default_permissions = ('view', 'add', 'change', 'delete')

