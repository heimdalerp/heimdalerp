from rest_framework.serializers import (HyperlinkedIdentityField,
                                        HyperlinkedModelSerializer,
                                        PrimaryKeyRelatedField)

from contact.serializers import ContactSerializer
from invoice import models
from persons.serializers import CompanySerializer


class FiscalPositionSerializer(HyperlinkedModelSerializer):
    companies = HyperlinkedIdentityField(
        view_name='api:invoice:fiscalposition-companies'
    )
    contacts = HyperlinkedIdentityField(
        view_name='api:invoice:fiscalposition-contacts'
    )

    class Meta:
        model = models.FiscalPosition
        fields = (
            'url',
            'id',
            'name',
            'companies',
            'contacts'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:fiscalposition-detail'
            }
        }


class ContactInvoiceSerializer(HyperlinkedModelSerializer):
    contact = ContactSerializer()
    fiscal_position = PrimaryKeyRelatedField(
        queryset=models.FiscalPosition.objects.all()
    )
    invoices = HyperlinkedIdentityField(
        view_name='api:invoice:contact-invoices'
    )

    class Meta:
        model = models.Contact
        fields = (
            'url',
            'id',
            'contact',
            'fiscal_position',
            'invoices'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:contact-detail'
            }
        }


class CompanyInvoiceSerializer(HyperlinkedModelSerializer):
    company = CompanySerializer()
    fiscal_position = PrimaryKeyRelatedField(
        queryset=models.FiscalPosition.objects.all()
    )
    contacts = HyperlinkedIdentityField(
        view_name='api:invoice:company-contacts'
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
            'fiscal_position',
            'contacts',
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
    vat = PrimaryKeyRelatedField(
        queryset=models.VAT.objects.all()
    )
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
                'view_name': 'api:invoice:product-detail'
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
            'contacts',
            'number',
            'invoice_lines',
            'invoice_date',
            'notes',
            'subtotal',
            'total',
            'status'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:invoice-detail'
            },
            'company': {
                'view_name': 'api:invoice:company-detail'
            },
            'contacts': {
                'view_name': 'api:invoice:contact-detail',
                'many': True
            }
        }
