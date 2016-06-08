from rest_framework.serializers import (HyperlinkedIdentityField,
                                        HyperlinkedModelSerializer)

from contact.models import Contact
from contact.serializers import ContactSerializer
from invoice import models
from persons.models import Company, PhysicalAddress
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
            'code',
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
            },
            'fiscal_position': {
                'view_name': 'api:invoice:fiscalposition-detail'
            }
        }

    def create(self, validated_data):
        contact_contact_data = validated_data.pop('contact_contact')
        home_address_data = contact_contact_data.pop('home_address')
        home_address, created = PhysicalAddress.objects.update_or_create(
            pk=home_address_data.get('id'),
            defaults=home_address_data
        )
        contact_contact_data['home_address'] = home_address

        contact_contact, created = Contact.objects.update_or_create(
            pk=contact_contact_data.get('id'),
            defaults=contact_contact_data
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
        instance.contact_contact.home_address.street_address = (
            home_address_data.get(
                'street_address',
                instance.contact_contact.home_address.street_address
            )
        )
        instance.contact_contact.home_address.floor_number = (
            home_address_data.get(
                'floor_number',
                instance.contact_contact.home_address.floor_number
            )
        )
        instance.contact_contact.home_address.apartment_number = (
            home_address_data.get(
                'apartment_number',
                instance.contact_contact.home_address.apartment_number
            )
        )
        instance.contact_contact.home_address.city = (
            home_address_data.get(
                'city',
                instance.contact_contact.home_address.city
            )
        )
        instance.contact_contact.home_address.postal_code = (
            home_address_data.get(
                'postal_code',
                instance.contact_contact.home_address.postal_code
            )
        )
        instance.contact_contact.home_address.save()

        instance.contact_contact.birth_date = contact_contact_data.get(
            'birth_date',
            instance.contact_contact.birth_date
        )
        instance.contact_contact.born_in = contact_contact_data.get(
            'born_in',
            instance.contact_contact.born_in
        )
        instance.contact_contact.phone_numbers = contact_contact_data.get(
            'phone_numbers',
            instance.contact_contact.phone_numbers
        )
        instance.contact_contact.extra_emails = contact_contact_data.get(
            'extra_emails',
            instance.contact_contact.extra_emails
        )
        instance.contact_contact.name = contact_contact_data.get(
            'name',
            instance.contact_contact.name
        )
        instance.contact_contact.contact_type = contact_contact_data.get(
            'contact_type',
            instance.contact_contact.contact_type
        )
        instance.contact_contact.save()

        fiscal_address_data = validated_data.pop('fiscal_address')
        instance.fiscal_address.street_address = fiscal_address_data.get(
            'street_address', instance.fiscal_address.street_address
        )
        instance.fiscal_address.floor_number = fiscal_address_data.get(
            'floor_number', instance.fiscal_address.floor_number
        )
        instance.fiscal_address.apartment_number = fiscal_address_data.get(
            'apartment_number', instance.fiscal_address.apartment_number
        )
        instance.fiscal_address.city = fiscal_address_data.get(
            'city', instance.fiscal_address.city
        )
        instance.fiscal_address.postal_code = fiscal_address_data.get(
            'postal_code', instance.fiscal_address.postal_code
        )
        instance.fiscal_address.save()

        instance.fiscal_position = validated_data.get(
            'fiscal_position', instance.fiscal_position
        )

        instance.save()
        return instance


class CompanyInvoiceSerializer(HyperlinkedModelSerializer):
    persons_company = CompanySerializer()
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
            'id',
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
            },
            'fiscal_position': {
                'view_name': 'api:invoice:fiscalposition-detail',
                'allow_null': True
            },
            'fiscal_addresses': {
                'required': False
            }
        }

    def create(self, validated_data):
        persons_company_data = validated_data.pop('persons_company')
        persons_company, created = Company.objects.update_or_create(
            pk=persons_company_data.get('id'),
            defaults=persons_company_data
        )
        validated_data['persons_company'] = persons_company

        company = models.CompanyInvoice.objects.create(**validated_data)
        return company

    def update(self, instance, validated_data):
        persons_company_data = validated_data.pop('persons_company')
        instance.persons_company.name = persons_company_data.get(
            'name',
            instance.persons_company.name
        )
        instance.persons_company.initiated_activities = (
            persons_company_data.get(
                'initiated_activities',
                instance.persons_company.initiated_activities
            )
        )
        instance.persons_company.save()

        instance.fiscal_position = validated_data.get(
            'fiscal_position',
            instance.fiscal_position
        )

        instance.save()
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
            },
            'vat': {
                'view_name': 'api:invoice:vat-detail'
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


class InvoiceTypeSerializer(HyperlinkedModelSerializer):
    invoices = HyperlinkedIdentityField(
        view_name='api:invoice:invoicetype-invoices'
    )

    class Meta:
        model = models.InvoiceType
        fields = (
            'url',
            'id',
            'name',
            'code',
            'invoices'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:invoicetype-detail'
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
            'invoice_type',
            'invoice_date',
            'notes',
            'subtotal',
            'total',
            'status',
            'transaction'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:invoice-detail'
            },
            'invoice_type': {
                'view_name': 'api:invoice:invoicetype-detail',
                'required': False,
                'allow_null': True
            },
            'company': {
                'view_name': 'api:invoice:companyinvoice-detail'
            },
            'contacts': {
                'view_name': 'api:invoice:contactinvoice-detail',
                'many': True
            },
            'transaction': {
                'view_name': 'api:accounting:transaction-detail',
                'required': False,
                'allow_null': True
            }
        }
