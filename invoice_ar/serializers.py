from rest_framework.serializers import HyperlinkedModelSerializer
                                        
from contact.models import Contact
from invoice.serializers import (CompanyInvoiceSerializer,
                                 ContactInvoiceSerializer,
                                 InvoiceLineSerializer)
from invoice.models import CompanyInvoice, ContactInvoice
from invoice_ar import models
from persons.models import Company, PhysicalAddress


class ContactInvoiceARSerializer(HyperlinkedModelSerializer):
    invoice_contact = ContactInvoiceSerializer()

    class Meta:
        model = models.ContactInvoiceAR
        fields = (
            'url',
            'id',
            'invoice_contact',
            'id_type',
            'id_number'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice_ar:contactinvoicear-detail'
            }
        }

    def create(self, validated_data):
        invoice_contact_data = validated_data['invoice_contact']
        contact_contact_data = invoice_contact_data.pop('contact_contact')
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
        invoice_contact_data['contact_contact'] = contact_contact

        fiscal_address_data = invoice_contact_data.pop('fiscal_address')
        fiscal_address, created = PhysicalAddress.objects.update_or_create(
            pk=fiscal_address_data.get('id'),
            defaults=fiscal_address_data
        )
        invoice_contact_data['fiscal_address'] = fiscal_address
        invoice_contact, created = ContactInvoice.objects.update_or_create(
            pk=invoice_contact_data.get('id'),
            defaults=invoice_contact_data
        )
        validated_data['invoice_contact'] = invoice_contact
        
        invoicear_contact = models.ContactInvoiceAR.objects.create(
            **validated_data
        )
        return invoicear_contact

    def update(self, instance, validated_data):
        invoice_contact_data = validated_data.pop('invoice_contact')
        contact_contact_data = invoice_contact_data.pop('contact_contact')
        home_address_data = contact_contact_data.pop('home_address')

        invoice_contact = instance.invoice_contact
        contact_contact = instance.invoice_contact.contact_contact

        contact_contact.home_address.street_address = (
            home_address_data.get(
                'street_address',
                contact_contact.home_address.street_address
            )
        )
        contact_contact.home_address.floor_number = (
            home_address_data.get(
                'floor_number',
                contact_contact.home_address.floor_number
            )
        )
        contact_contact.home_address.apartment_number = (
            home_address_data.get(
                'apartment_number',
                contact_contact.home_address.apartment_number
            )
        )
        contact_contact.home_address.city = (
            home_address_data.get(
                'city',
                contact_contact.home_address.city
            )
        )
        contact_contact.home_address.postal_code = (
            home_address_data.get(
                'postal_code',
                contact_contact.home_address.postal_code
            )
        )
        contact_contact.home_address.save()

        contact_contact.birth_date = contact_contact_data.get(
            'birth_date',
            contact_contact.birth_date
        )
        contact_contact.born_in = contact_contact_data.get(
            'born_in',
            contact_contact.born_in
        )
        contact_contact.phone_numbers = contact_contact_data.get(
            'phone_numbers',
            contact_contact.phone_numbers
        )
        contact_contact.extra_emails = contact_contact_data.get(
            'extra_emails',
            contact_contact.extra_emails
        )
        contact_contact.name = contact_contact_data.get(
            'name',
            contact_contact.name
        )
        contact_contact.contact_type = contact_contact_data.get(
            'contact_type',
            contact_contact.contact_type
        )
        contact_contact.save()

        fiscal_address_data = invoice_contact_data.pop('fiscal_address')
        invoice_contact.fiscal_address.street_address = (
            fiscal_address_data.get(
                'street_address',
                invoice_contact.fiscal_address.street_address
            )
        )
        invoice_contact.fiscal_address.floor_number = (
            fiscal_address_data.get(
                'floor_number',
                invoice_contact.fiscal_address.floor_number
            )
        )
        invoice_contact.fiscal_address.apartment_number = (
            fiscal_address_data.get(
                'apartment_number',
                invoice_contact.fiscal_address.apartment_number
            )
        )
        invoice_contact.fiscal_address.city = (
            fiscal_address_data.get(
                'city',
                invoice_contact.fiscal_address.city
            )
        )
        invoice_contact.fiscal_address.postal_code = (
            fiscal_address_data.get(
                'postal_code',
                invoice_contact.fiscal_address.postal_code
            )
        )
        invoice_contact.fiscal_address.save()

        instance.id_type = validated_data.get('id_type', instance.id_type)
        instance.id_number = validated_data.get(
            'id_number', instance.id_number
        )

        instance.save()
        return instance


class CompanyInvoiceARSerializer(HyperlinkedModelSerializer):
    invoice_company = CompanyInvoiceSerializer()

    class Meta:
        model = models.CompanyInvoiceAR
        fields = (
            'url',
            'id',
            'invoice_company',
            'cuit',
            'iibb'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice_ar:companyinvoicear-detail'
            }
        }

    def create(self, validated_data):
        invoice_company_data = validated_data.pop('invoice_company')
        persons_company_data = invoice_company_data.pop('persons_company')
        persons_company, created = Company.objects.update_or_create(
            pk=persons_company_data.get('id'),
            defaults=persons_company_data
        )
        invoice_company_data['persons_company'] = persons_company

        fiscal_address_data = invoice_company_data.pop('fiscal_address')
        fiscal_address, created = PhysicalAddress.objects.update_or_create(
            pk=fiscal_address_data.get('id'),
            defaults=fiscal_address_data
        )
        invoice_company_data['fiscal_address'] = fiscal_address

        invoice_company, created = CompanyInvoice.objects.update_or_create(
            pk=invoice_company_data.get('id'),
            defaults=invoice_company_data
        )
        validated_data['invoice_company'] = invoice_company

        company = models.CompanyInvoiceAR.objects.create(**validated_data)
        return company

    def update(self, instance, validated_data):
        invoice_company_data = validated_data.pop('invoice_company')
        persons_company_data = invoice_company_data.pop('persons_company')
        fiscal_address_data = invoice_company_data.pop('fiscal_address')

        invoice_company = instance.invoice_company
        persons_company = instance.invoice_company.persons_company

        persons_company.name = persons_company_data.get(
            'name',
            persons_company.name
        )
        persons_company.initiated_activities = (
            persons_company_data.get(
                'initiated_activities',
                persons_company.initiated_activities
            )
        )
        persons_company.save()

        invoice_company.fiscal_address.street_address = (
            fiscal_address_data.get(
                'street_address',
                invoice_company.fiscal_address.street_address
            )
        )
        invoice_company.fiscal_address.floor_number = (
            fiscal_address_data.get(
                'floor_number',
                invoice_company.fiscal_address.floor_number
            )
        )
        invoice_company.fiscal_address.apartment_number = (
            fiscal_address_data.get(
                'apartment_number',
                invoice_company.fiscal_address.apartment_number
            )
        )
        invoice_company.fiscal_address.city = (
            fiscal_address_data.get(
                'city',
                invoice_company.fiscal_address.city
            )
        )
        invoice_company.fiscal_address.postal_code = (
            fiscal_address_data.get(
                'postal_code',
                invoice_company.fiscal_address.postal_code
            )
        )
        invoice_company.fiscal_address.save()

        invoice_company.fiscal_position = validated_data.get(
            'fiscal_position',
            instance.fiscal_position
        )
        invoice_company.save()

        instance.cuit = validated_data.get('cuit', instance.cuit)
        instance.iibb = validated_data.get('iibb', instance.iibb)
        instance.save()
        return instance


class PointOfSaleSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.PointOfSale
        fields = (
            'url',
            'id',
            'invoicear_company',
            'afip_id',
            'point_of_sale_type',
            'fiscal_address',
            'is_inactive'
        ) 
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoicear:pointofsale-detail'
            },
            'invoicear_company': {
                'view_name': 'api:invoicear:companyinvoicear-detail'
            },
            'fiscal_address': {
                'view_name': 'api:persons:physicaladdress-detail'
            }
        }


class InvoiceTypeSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.InvoiceType
        fields = (
            'url',
            'id',
            'name',
            'afip_code'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoicear:invoicetype-detail'
            }
        }


class VATSubtotalSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.InvoiceARHasVATSubtotal
        fields = (
            'url',
            'id',
            'vat',
            'subtotal'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoicear:invoicearhasvatsubtotal-detail'
            },
            'vat': {
                'view_name': 'api:invoice:vat-detail'
            }
        }


class InvoiceARSerializer(HyperlinkedModelSerializer):
    invoice_lines = InvoiceLineSerializer(many=True)
    vat_subtotals = VATSubtotalSerializer(many=True)

    class Meta:
        model = models.InvoiceAR
        fields = (
            'url',
            'id',
            'invoice_company',
            'contacts',
            'number',
            'invoice_lines',
            'invoice_date',
            'status',
            'subtotal',
            'total',
            'notes',
            'point_of_sale',
            'due_date',
            'service_start',
            'service_type',
            'vat_total',
            'vat_subtotals'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoicear:invoicear-detail'
            },
            'invoice_company': {
                'view_name': 'api:invoice:companyinvoice-detail'
            },
            'contacts': {
                'view_name': 'api:invoice:contactinvoice-detail',
                'many': True
            },
            'point_of_sale': {
                'view_name': 'api:invoicear:pointofsale-detail'
            }
        }
