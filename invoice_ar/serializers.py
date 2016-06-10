from rest_framework.serializers import (HyperlinkedIdentityField,
                                        HyperlinkedModelSerializer)

from contact.models import Contact
from invoice.models import (INVOICE_STATUSTYPE_DRAFT, CompanyInvoice,
                            ContactInvoice)
from invoice.serializers import (CompanyInvoiceSerializer,
                                 ContactInvoiceSerializer,
                                 InvoiceLineSerializer)
from invoice_ar import models
from persons.models import Company, PhysicalAddress


class ContactInvoiceARSerializer(HyperlinkedModelSerializer):
    invoice_contact = ContactInvoiceSerializer()
    invoices = HyperlinkedIdentityField(
        view_name='api:invoice_ar:contactinvoicear-invoices'
    )

    class Meta:
        model = models.ContactInvoiceAR
        fields = (
            'url',
            'id',
            'invoice_contact',
            'id_type',
            'id_number',
            'invoices'
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
        invoice_contact.fiscal_position = invoice_contact_data.get(
            'fiscal_position',
            invoice_contact.fiscal_position
        )
        invoice_contact.legal_name = invoice_contact_data.get(
            'legal_name',
            invoice_contact.legal_name
        )
        invoice_contact.save()

        instance.id_type = validated_data.get('id_type', instance.id_type)
        instance.id_number = validated_data.get(
            'id_number', instance.id_number
        )

        instance.save()
        return instance


class CompanyInvoiceARSerializer(HyperlinkedModelSerializer):
    invoice_company = CompanyInvoiceSerializer()
    invoices = HyperlinkedIdentityField(
        view_name='api:invoice_ar:companyinvoicear-invoices'
    )

    class Meta:
        model = models.CompanyInvoiceAR
        fields = (
            'url',
            'id',
            'invoice_company',
            'cuit',
            'iibb',
            'invoices'
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
            pk=persons_company_data.get('pk'),
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
            pk=invoice_company_data.get('pk'),
            defaults=invoice_company_data
        )
        validated_data['invoice_company'] = invoice_company

        company = models.CompanyInvoiceAR.objects.create(**validated_data)
        return company

    def update(self, instance, validated_data):
        invoice_company_data = validated_data.pop('invoice_company')
        persons_company_data = invoice_company_data.pop('persons_company')

        invoice_company = instance.invoice_company
        persons_company = instance.invoice_company.persons_company

        persons_company.fantasy_name = persons_company_data.get(
            'fantasy_name',
            persons_company.fantasy_name
        )
        persons_company.legal_name = persons_company_data.get(
            'legal_name',
            persons_company.legal_name
        )

        persons_company.initiated_activities = (
            persons_company_data.get(
                'initiated_activities',
                persons_company.initiated_activities
            )
        )
        persons_company.save()

        fiscal_address_data = invoice_company_data.pop('fiscal_address')
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
            invoice_company.fiscal_position
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
                'view_name': 'api:invoice_ar:pointofsale-detail'
            },
            'invoicear_company': {
                'view_name': 'api:invoice_ar:companyinvoicear-detail'
            },
            'fiscal_address': {
                'view_name': 'api:persons:physicaladdress-detail'
            }
        }


class InvoiceARHasVATSubtotalSerializer(HyperlinkedModelSerializer):

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
                'view_name': 'api:invoice_ar:invoicearhasvatsubtotal-detail'
            },
            'vat': {
                'view_name': 'api:invoice:vat-detail'
            }
        }


class ConceptTypeSerializer(HyperlinkedModelSerializer):
    invoices = HyperlinkedIdentityField(
        view_name='api:invoice_ar:concepttype-invoices'
    )

    class Meta:
        model = models.ConceptType
        fields = (
            'url',
            'id',
            'name',
            'code',
            'invoices'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice_ar:concepttype-detail'
            }
        }


class InvoiceARSerializer(HyperlinkedModelSerializer):
    invoice_lines = InvoiceLineSerializer(many=True)
    vat_subtotals = InvoiceARHasVATSubtotalSerializer(many=True)

    class Meta:
        model = models.InvoiceAR
        fields = (
            'url',
            'id',
            'invoicear_company',
            'invoicear_contact',
            'number',
            'invoice_lines',
            'invoice_type',
            'invoice_date',
            'status',
            'subtotal',
            'total',
            'notes',
            'transaction',
            'point_of_sale',
            'due_date',
            'service_start',
            'concept_type',
            'vat_total',
            'vat_subtotals'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice_ar:invoicear-detail'
            },
            'invoicear_company': {
                'view_name': 'api:invoice_ar:companyinvoice-detail'
            },
            'invoice_type': {
                'view_name': 'api:invoice:invoicetype-detail'
            },
            'invoicear_contact': {
                'view_name': 'api:invoice_ar:contactinvoice-detail'
            },
            'status': {
                'read_only': True
            },
            'subtotal': {
                'read_only': True
            },
            'total': {
                'read_only': True
            },
            'transaction': {
                'view_name': 'api:accounting:transaction-detail',
                'read_only': True
            },
            'point_of_sale': {
                'view_name': 'api:invoice_ar:pointofsale-detail'
            },
            'concept_type': {
                'view_name': 'api:invoice_ar:concepttype-detail'
            },
            'vat_total': {
                'read_only': True
            },
            'vat_subtotals': {
                'view_name':
                    'api:invoice_ar:invoicearhasvatsubtotal-detail',
                'many': True,
                'read_only': True
            }
        }

    def create(self, validated_data):
        invoice_company = (
            validated_data.get('invoicear_company').invoice_company
        )
        invoice_contact = (
            validated_data.get('invoicear_contact').invoice_contact
        )

        invoicear = models.InvoiceAR.create(
            status=INVOICE_STATUSTYPE_DRAFT,
            invoice_company=invoice_company,
            invoice_contact=invoice_contact,
            **validated_data
        )
        return invoicear
