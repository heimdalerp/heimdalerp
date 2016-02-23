from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.serializers import HyperlinkedIdentityField

from persons.serializers import PhoneNumberSerializer
from persons.serializers import ExtraEmailAddressSerializer
from persons.serializers import PhysicalAddressSerializer
from invoice import models

class FiscalPositionSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.FiscalPosition
        fields = (
            'url',
            'id',
            'name'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:fiscalposition-detail'
            }
        }


class ClientSerializer(HyperlinkedModelSerializer):
    fiscal_position = FiscalPositionSerializer()

    class Meta:
        model = models.Client
        fields = (
            'url',
            'id',
            'name',
            'client_type',
            'fiscal_position'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:client-detail'
            }
        }


class CompanySerializer(HyperlinkedModelSerializer):
    fiscal_position = FiscalPositionSerializer()
    employees = HyperlinkedIdentityField(
        view_name='api:invoice:company-employees'
    )
    clients = HyperlinkedIdentityField(
        view_name='api:invoice:company-clients'
    )
    invoices = HyperlinkedIdentityField(
        view_name='api:invoice:company-invoices'
    )

    class Meta:
        model = models.Company
        fields = (
            'url',
            'id',
            'name',
            'initiated_activities',
            'fiscal_position',
            'employees',
            'clients'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:company-detail'
            }
        }


class VAT(HyperlinkedModelSerializer):

    class Meta:
        model = models.VAT
        fields = (
            'url',
            'id',
            'name',
            'tax'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:vat-detail'
            }
        }


class InvoiceProduct(HyperlinkedModelSerializer):
    vat = VATSerializer()

    class Meta:
        model = models.InvoiceProduct
        fields = (
            'url',
            'id',
            'company',
            'name',
            'suggested_price',
            'vat'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:invoiceproduct-detail'
            },
            'company': {
                'view_name': 'api:invoice:company-detail'
            }
        }


class InvoiceLine(HyperlinkedModelSerializer):

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


class Invoice(HyperlinkedModelSerializer):
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


