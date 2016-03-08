from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.serializers import HyperlinkedIdentityField

from persons.serializers import CompanySerializer
from invoice import models


class FiscalPositionSerializer(HyperlinkedModelSerializer):
    companies = HyperlinkedIdentityField(
        view_name='api:invoice:fiscalposition-companies'
    )
    clients = HyperlinkedIdentityField(
        view_name='api:invoice:fiscalposition-clients'
    )

    class Meta:
        model = models.FiscalPosition
        fields = (
            'url',
            'id',
            'name',
            'companies',
            'clients'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:fiscalposition-detail'
            }
        }


class ClientSerializer(HyperlinkedModelSerializer):
    fiscal_position = FiscalPositionSerializer()
    invoices = HyperlinkedIdentityField(
        view_name='api:invoice:client-invoices'
    )
    companies = HyperlinkedIdentityField(
        view_name='api:invoice:client-companies'
    )

    class Meta:
        model = models.Client
        fields = (
            'url',
            'id',
            'name',
            'client_type',
            'fiscal_position',
            'invoices',
            'companies'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:client-detail'
            }
        }


class CompanyInvoiceSerializer(HyperlinkedModelSerializer):
    company = CompanySerializer()
    fiscal_position = FiscalPositionSerializer()
    clients = HyperlinkedIdentityField(
        view_name='api:invoice:company-clients'
    )
    products = HyperlinkedIdentityField(
        view_name='api:invoice:company-products'
    )
    invoices = HyperlinkedIdentityField(
        view_name='api:invoice:company-invoices'
    )

    class Meta:
        model = models.CompanyInvoice
        fields = (
            'url',
            'company',
            'initiated_activities',
            'fiscal_position',
            'clients',
            'products',
            'invoices'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:company-detail'
            }
        }


class VATSerializer(HyperlinkedModelSerializer):
    products = HyperlinkedIdentityField(
        view_name='api:invoice:vat-products'
    )

    class Meta:
        model = models.VAT
        fields = (
            'url',
            'id',
            'name',
            'tax',
            'products'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:vat-detail'
            }
        }


class ProductSerializer(HyperlinkedModelSerializer):
    vat = VATSerializer()
    invoice_lines = HyperlinkedIdentityField(
        view_name='api:invoice:product-invoicelines'
    )

    class Meta:
        model = models.Product
        fields = (
            'url',
            'id',
            'company',
            'name',
            'suggested_price',
            'vat',
            'invoice_lines'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:product-detail'
            },
            'company': {
                'view_name': 'api:invoice:company-detail'
            }
        }


class InvoiceLineSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.InvoiceLine
        fields = (
            'url',
            'id',
            'product',
            'product_price_override',
            'product_vat_override',
            'product_discount',
            'quantity'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:invoiceline-detail'
            },
            'product': {
                'view_name': 'api:invoice:invoiceproduct-detail'
            }
        }


class InvoiceSerializer(HyperlinkedModelSerializer):
    invoice_lines = InvoiceLineSerializer(many=True)

    class Meta:
        model = models.Invoice
        fields = (
            'url',
            'id',
            'company',
            'clients',
            'number',
            'invoice_lines',
            'invoice_date',
            'notes',
            'subtotal',
            'total'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:invoice-detail'
            },
            'company': {
                'view_name': 'api:invoice:company-detail'
            },
            'clients': {
                'view_name': 'api:invoice:client-detail',
                'many': True
            }
        }
