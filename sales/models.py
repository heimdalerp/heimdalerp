from django.db import models
from django.utils.translation import ugettext_lazy as _

from persons.models import Company
from hr.models import Employee
from invoice.models import Client, Product, VAT


class ProductCategory(models.Model):
    """
    A product may have one or more categories.
    """
    company = models.ForeignKey(
        Company,
        verbose_name=_('company'),
        related_name='product_categories',
        related_query_name='product_category'
    )
    name = models.CharField(
        _('name'),
        max_length=50
    )
    description = models.TextField(
        _('description'),
        max_length=200,
        blank=True,
        default=""
    )

    def __str__(self):
        return "%(name)s" % {'name': self.name}

    class Meta:
        unique_together = (('company', 'name'), )
        index_together = [['company', 'name'], ]
        verbose_name = _('product category')
        verbose_name_plural = _('product categories')
        default_permissions = ('view', 'add', 'change', 'delete')


class ProductSales(models.Model):
    """
    An extension of Product defined in 'invoice'.
    """
    product = models.OneToOneField(Product)
    description = models.TextField(
        _('description'),
        max_length=500,
        blank=True,
        default=""
    ) 
    categories = models.ManyToManyField(
        ProductCategory,
        verbose_name=_('categories'),
        related_name='products',
        related_query_name='product',
        blank=True
    )

    def __str__(self):
        return self.product

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        default_permissions = ('view', 'add', 'change', 'delete')


class QuotationLine(models.Model):
    """
    A quotation is composed of lines or entries, which have a product,
    a price and a quantity.
    """
    product = models.ForeignKey(
        ProductSales,
        verbose_name=_('product'),
        related_name='quotation_lines',
        related_query_name='quotation_line'
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
        related_name='quotation_lines',
        related_query_name='quotation_line',
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
        verbose_name = _('quotation line')
        verbose_name_plural = _('quotation lines')
        default_permissions = ('view', 'add', 'change', 'delete')


class Quotation(models.Model):
    """
    A quotation is a previous step to a sale.
    It should be fairly similar to a sale and to an invoice.
    """
    company = models.ForeignKey(
        Company,
        verbose_name=_('company'),
        related_name='quotations',
        related_query_name='quotation',
        db_index=True
    )
    clients = models.ManyToManyField(
        Client,
        verbose_name=_('clients'),
        related_name='quotations',
        related_query_name='quotation'
    ) 
    quotation_lines = models.ManyToManyField(
        QuotationLine,
        verbose_name=_('quotation lines'),
        related_name='+',
        related_query_name='quotation'
    )
    quotation_date = models.DateField(
        _('date'),
        help_text=_('Not necessarily today.')
    )
    subtotal = models.DecimalField(
        _('subtotal'),
        max_digits=12,
        decimal_places=2,
        default=0.00,
        help_text=_('Total without taxes.')
    )
    total = models.DecimalField(
        _('total'),
        max_digits=12,
        decimal_places=2,
        default=0.00,
        help_text=_('Subtotal plus taxes.')
    )
    notes = models.TextField(
        _('notes'),
        blank=True,
        default=""
    )

    def __str__(self):
        return "%(company)s : %(pk)s" % {
            'company': self.company,
            'pk': self.pk
        }

    class Meta:
        verbose_name = _('quotation')
        verbose_name_plural = _('quotations')
        default_permissions = ('view', 'add', 'change', 'delete')


class SaleLine(models.Model):
    """
    A sale is composed of lines or entries, which have a product,
    a price and a quantity.
    """
    product = models.ForeignKey(
        ProductSales,
        verbose_name=_('product'),
        related_name='sale_lines',
        related_query_name='sale_line'
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
        related_name='sale_lines',
        related_query_name='sale_line',
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
        verbose_name = _('sale line')
        verbose_name_plural = _('sale lines')
        default_permissions = ('view', 'add', 'change', 'delete')


class Sale(models.Model):
    """
    A sale is a previous step to an invoice.
    """
    quotation = models.OneToOneField(
        Quotation,
        verbose_name=_('quotation'),
        blank=True,
        null=True
    )
    company = models.ForeignKey(
        Company,
        verbose_name=_('company'),
        related_name='sales',
        related_query_name='sale',
        db_index=True
    )
    clients = models.ManyToManyField(
        Client,
        verbose_name=_('clients'),
        related_name='sales',
        related_query_name='sale'
    ) 
    sale_lines = models.ManyToManyField(
        SaleLine,
        verbose_name=_('sales lines'),
        related_name='+',
        related_query_name='sale'
    )
    quotation_date = models.DateField(
        _('date'),
        help_text=_('Not necessarily today.')
    )
    subtotal = models.DecimalField(
        _('subtotal'),
        max_digits=12,
        decimal_places=2,
        default=0.00,
        help_text=_('Total without taxes.')
    )
    total = models.DecimalField(
        _('total'),
        max_digits=12,
        decimal_places=2,
        default=0.00,
        help_text=_('Subtotal plus taxes.')
    )
    notes = models.TextField(
        _('notes'),
        blank=True,
        default=""
    )

    def __str__(self):
        return "%(company)s : %(pk)s" % {
            'company': self.company,
            'pk': self.pk
        }

    class Meta:
        verbose_name = _('sale')
        verbose_name_plural = _('sales')
        default_permissions = ('view', 'add', 'change', 'delete')
