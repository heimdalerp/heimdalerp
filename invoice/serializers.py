from rest_framework.serializers import (HyperlinkedIdentityField,
                                        HyperlinkedModelSerializer,
                                        PrimaryKeyRelatedField)

from contact.models import Contact
from contact.serializers import ContactSerializer
from invoice import models
from persons.models import PhysicalAddress
from persons.serializers import CompanySerializer, PhysicalAddressSerializer


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
    contact_contact = ContactSerializer()
    fiscal_position = PrimaryKeyRelatedField(
        queryset=models.FiscalPosition.objects.all()
    )
    fiscal_address = PhysicalAddressSerializer()
    invoices = HyperlinkedIdentityField(
        view_name='api:invoice:contactinvoice-invoices'
    )

    class Meta:
        model = models.ContactInvoice
        fields = (
            'url',
            'id',
            'contact_contact',
            'fiscal_position',
            'fiscal_address',
            'invoices'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:contactinvoice-detail'
            }
        }

    def create(self, validated_data):
        contact_contact_data = validated_data.pop('contact_contact')
        home_address_data = contact_contact_data.pop('home_address')
        home_address = PhysicalAddress.objects.update_or_create(
            **home_address_data
        )
        contact_contact_data['home_address'] = home_address

        contact_contact = Contact.objects.update_or_create(
            **contact_contact_data
        )
        validated_data['contact_contact'] = contact_contact

        fiscal_address_data = validated_data.pop('fiscal_address')
        fiscal_address = PhysicalAddress.objects.create(
            **fiscal_address_data
        )
        validated_data['fiscal_address'] = fiscal_address
        invoice_contact = models.ContactInvoice.objects.create(
            **validated_data
        )
        return invoice_contact

    def update(self, instance, validated_data):
        contact_contact_data = validated_data.pop('contact_contact')
        home_address_data = contact_contact_data.pop('home_address')
        home_address = PhysicalAddress.objects.update_or_create(
            **home_address_data
        )
        contact_contact_data['home_address'] = home_address

        contact_contact = Contact.objects.update_or_create(
            **contact_contact_data
        )
        validated_data['contact_contact'] = contact_contact

        fiscal_address_data = validated_data.pop('fiscal_address')
        fiscal_address = PhysicalAddress.objects.update_or_create(
            **fiscal_address_data
        )
        validated_data['fiscal_address'] = fiscal_address
        instance.update(**validated_data)
        return instance


class CompanyInvoiceSerializer(HyperlinkedModelSerializer):
    persons_company = CompanySerializer()
    fiscal_position = PrimaryKeyRelatedField(
        queryset=models.FiscalPosition.objects.all()
    )
    fiscal_address = PhysicalAddressSerializer()
    contacts = HyperlinkedIdentityField(
        view_name='api:invoice:companyinvoice-contacts'
    )
    products = HyperlinkedIdentityField(
        view_name='api:invoice:companyinvoice-products'
    )
    invoices = HyperlinkedIdentityField(
        view_name='api:invoice:companyinvoice-invoices'
    )

    class Meta:
        model = models.CompanyInvoice
        fields = (
            'url',
            'persons_company',
            'fiscal_position',
            'fiscal_address',
            'contacts',
            'products',
            'invoices'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:companyinvoice-detail'
            }
        }

    def create(self, validated_data):
        fiscal_address_data = validated_data.pop('fiscal_address')
        fiscal_address = PhysicalAddress.objects.create(
            **fiscal_address_data
        )
        validated_data['fiscal_address'] = fiscal_address
        company = models.CompanyInvoice.objects.create(**validated_data)
        return company

    def update(self, instance, validated_data):
        fiscal_address_data = validated_data.pop('fiscal_address')
        fiscal_address = PhysicalAddress.objects.update_or_create(
            **fiscal_address_data
        )
        validated_data['fiscal_address'] = fiscal_address
        instance.update(**validated_data)
        return instance


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
                'view_name': 'api:invoice:companyinvoice-detail'
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
                'view_name': 'api:invoice:companyinvoice-detail'
            },
            'contacts': {
                'view_name': 'api:invoice:contactinvoice-detail',
                'many': True
            }
        }
