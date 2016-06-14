from decimal import Decimal

from django.db import transaction
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
            'legal_name',
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

    @transaction.atomic
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

    @transaction.atomic
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
        instance.legal_name = validated_data.get(
            'legal_name', instance.legal_name
        )

        instance.save()
        return instance


class CompanyInvoiceSerializer(HyperlinkedModelSerializer):
    persons_company = CompanySerializer()
    fiscal_address = PhysicalAddressSerializer()
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
            'products',
            'default_invoice_debit_account',
            'default_invoice_credit_account',
            'invoices'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:companyinvoice-detail'
            },
            'fiscal_position': {
                'view_name': 'api:invoice:fiscalposition-detail',
                'required': False,
                'allow_null': True
            },
            'fiscal_address': {
                'required': False
            },
            'default_invoice_debit_account': {
                'view_name': 'api:accounting:account-detail',
                'required': False,
                'allow_null': True
            },
            'default_invoice_credit_account': {
                'view_name': 'api:accounting:account-detail',
                'required': False,
                'allow_null': True
            }
        }

    @transaction.atomic
    def create(self, validated_data):
        persons_company_data = validated_data.pop('persons_company')
        persons_company, created = Company.objects.update_or_create(
            pk=persons_company_data.get('id'),
            defaults=persons_company_data
        )
        validated_data['persons_company'] = persons_company

        fiscal_address_data = validated_data.pop('fiscal_address')
        fiscal_address = PhysicalAddress.objects.create(
            **fiscal_address_data
        )
        validated_data['fiscal_address'] = fiscal_address

        company = models.CompanyInvoice.objects.create(**validated_data)
        return company

    @transaction.atomic
    def update(self, instance, validated_data):
        persons_company_data = validated_data.pop('persons_company')

        instance.persons_company.fantasy_name = persons_company_data.get(
            'fantasy_name',
            instance.persons_company.fantasy_name
        )
        instance.persons_company.legal_name = persons_company_data.get(
            'legal_name',
            instance.persons_company.legal_name
        )
        instance.persons_company.initiated_activities = (
            persons_company_data.get(
                'initiated_activities',
                instance.persons_company.initiated_activities
            )
        )
        instance.persons_company.save()

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
            'fiscal_position',
            instance.fiscal_position
        )
        instance.default_invoice_debit_account = validated_data.get(
            'default_invoice_debit_account',
            instance.default_invoice_debit_account
        )
        instance.default_invoice_credit_account = validated_data.get(
            'default_invoice_credit_account',
            instance.default_invoice_credit_account
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
            'code',
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
            'invoice_company',
            'name',
            'current_price',
            'vat',
            'invoice_lines'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice:product-detail'
            },
            'invoice_company': {
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
            'price_sold',
            'discount',
            'quantity',
            'description'
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
            'invoice_company',
            'invoice_contact',
            'number',
            'invoice_lines',
            'invoice_type',
            'invoice_date',
            'notes',
            'subtotal',
            'total',
            'status',
            'invoice_debit_account',
            'invoice_credit_account',
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
            'invoice_company': {
                'view_name': 'api:invoice:companyinvoice-detail'
            },
            'invoice_contact': {
                'view_name': 'api:invoice:contactinvoice-detail'
            },
            'number': {
                'required': False
            },
            'subtotal': {
                'read_only': True
            },
            'total': {
                'read_only': True
            },
            'status': {
                'read_only': True
            },
            'invoice_debit_account': {
                'view_name': 'api:accounting:account-detail',
                'required': False,
                'allow_null': True
            },
            'invoice_credit_account': {
                'view_name': 'api:accounting:account-detail',
                'required': False,
                'allow_null': True
            },
            'transaction': {
                'view_name': 'api:accounting:transaction-detail',
                'read_only': True
            }
        }

    @transaction.atomic
    def create(self, validated_data):
        '''
        number = validated_data.get('number')
        if number is None or number == 0:
            max_invoice = models.Invoice.objects.all.aggregate(
                models.Max('number')
            )
            number = max_invoice.number + 1
            validated_data['number'] = number
        '''
        validated_data['status'] = models.INVOICE_STATUSTYPE_DRAFT
        number = validated_data.get('number')
        if number is None or number == 0:
            validated_data['number'] = 0

        invoice_company = validated_data.get('invoice_company')
        if validated_data.get('invoice_debit_account') is None:
            validated_data['invoice_debit_account'] = (
                invoice_company.default_invoice_debit_account
            )
        if validated_data.get('invoice_credit_account') is None:
            validated_data['invoice_credit_account'] = (
                invoice_company.default_invoice_credit_account
            )

        invoice_lines_data = validated_data.pop('invoice_lines')

        invoice = models.Invoice.objects.create(
            **validated_data
        )

        if invoice_lines_data is not None:
            subtotal = Decimal('0.00')
            total = Decimal('0.00')
            for l_data in invoice_lines_data:
                l = models.InvoiceLine.objects.create(**l_data)
                if l.discount > 0.00:
                    price_aux = l.quantity * (
                        l.price_sold - (l.price_sold * l.discount)
                    )
                    subtotal += price_aux
                    total += (
                        price_aux + (price_aux * l.product.vat.tax)
                    )
                else:
                    subtotal += l.price_sold * l.quantity
                    total += l.quantity * (
                        l.price_sold + (l.price_sold * l.product.vat.tax)
                    )

                invoice.invoice_lines.add(l)

            invoice.subtotal = subtotal
            invoice.total = total
            invoice.save()

        return invoice

    @transaction.atomic
    def update(self, instance, validated_data):
        if instance.status is models.INVOICE_STATUSTYPE_DRAFT:
            instance.invoice_company = validated_data.get(
                'invoice_company',
                instance.invoice_company
            )
            instance.invoice_contact = validated_data.get(
                'invoice_contact',
                instance.invoice_contact
            )
            instance.invoice_date = validated_data.get(
                'invoice_date',
                instance.invoice_date
            )
            instance.notes = validated_data.get(
                'notes',
                instance.notes
            )
            instance.debit_account = validated_data.get(
                'invoice_debit_account',
                instance.invoice_debit_account
            )
            instance.invoice_credit_account = validated_data.get(
                'invoice_credit_account',
                instance.invoice_credit_account
            )

            invoice_lines_data = validated_data.get('invoice_lines')
            if invoice_lines_data is not None:
                subtotal = Decimal('0.00')
                total = Decimal('0.00')
                for l_data in invoice_lines_data:
                    l, created = (
                        models.InvoiceLine.objects.update_or_create(
                            pk=l_data.get('id'),
                            defaults=l_data
                        )
                    )
                    if created:
                        instance.invoice_lines.add(l)
                    if l.discount > 0.00:
                        price_aux = l.quantity * (
                            l.price_sold - (l.price_sold * l.discount)
                        )
                        subtotal += price_aux
                        total += (
                            price_aux + (price_aux * l.product.vat.tax)
                        )
                else:
                    subtotal += l.quantity * l.price_sold
                    total += l.quantity * (
                        l.price_sold + (l.price_sold * l.product.vat.tax)
                    )

                instance.subtotal = subtotal
                instance.total = total

            instance.save()

        return instance
