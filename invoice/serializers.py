from decimal import Decimal

from contact.models import Contact
from contact.serializers import ContactSerializer
from django.db import transaction
from invoice import models
from persons.models import Company, PhysicalAddress
from persons.serializers import CompanySerializer, PhysicalAddressSerializer
from rest_framework.serializers import (HyperlinkedIdentityField,
                                        HyperlinkedModelSerializer)


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
    def create(self, validated_data):  # TODO: Use existing objects.
        contact_contact_data = validated_data.pop('contact_contact')
        home_address_data = contact_contact_data.pop('home_address')
        home_address = PhysicalAddress.objects.create(
            **home_address_data
        )
        contact_contact_data['home_address'] = home_address

        contact_contact = Contact.objects.create(
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
        instance.contact_contact.home_address.locality = (
            home_address_data.get(
                'locality',
                instance.contact_contact.home_address.locality
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
        instance.fiscal_address.locality = fiscal_address_data.get(
            'locality', instance.fiscal_address.locality
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
            'legal_name',
            'initiated_activities',
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
    def create(self, validated_data):  # TODO: Use existing objects.
        persons_company_data = validated_data.pop('persons_company')
        persons_company = Company.objects.create(
            **persons_company_data
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
        instance.persons_company.slogan = persons_company_data.get(
            'slogan',
            instance.persons_company.slogan
        )
        instance.persons_company.save()
        instance.legal_name = validated_data.get(
            'legal_name',
            instance.legal_name
        )
        instance.initiated_activities = (
            validated_data.get(
                'initiated_activities',
                instance.initiated_activities
            )
        )

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
        instance.fiscal_address.locality = fiscal_address_data.get(
            'locality', instance.fiscal_address.locality
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
            },
            'tax': {
                'coerce_to_string': False
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
            },
            'current_price': {
                'coerce_to_string': False
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
            },
            'price_sold': {
                'coerce_to_string': False
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
            'invoice_type_class',
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
                'read_only': True,
                'coerce_to_string': False
            },
            'total': {
                'read_only': True,
                'coerce_to_string': False
            },
            'status': {
                'read_only': True
            },
            'transaction': {
                'view_name': 'api:accounting:transaction-detail',
                'read_only': True
            }
        }

    @transaction.atomic
    def create(self, validated_data):
        validated_data['status'] = models.INVOICE_STATUSTYPE_DRAFT
        number = validated_data.get('number')
        if number is None or number == 0:
            validated_data['number'] = 0

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
                    price_aux = Decimal(
                        l.quantity * (
                            l.price_sold - (l.price_sold * l.discount)
                        )
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
            instance.invoice_type = validated_data.get(
                'invoice_type',
                instance.invoice_type
            )
            instance.notes = validated_data.get(
                'notes',
                instance.notes
            )
            instance.number = validated_data.get(
                'number',
                instance.number
            )

            invoice_lines_data = validated_data.get('invoice_lines')
            if invoice_lines_data is not None:
                instance.invoice_lines.clear()
                subtotal = Decimal('0.00')
                total = Decimal('0.00')
                for l_data in invoice_lines_data:
                    l = models.InvoiceLine.objects.create(**l_data)
                    instance.invoice_lines.add(l)
                    if l.discount > 0.00:
                        price_aux = Decimal(
                            l.quantity * (
                                l.price_sold - (l.price_sold * l.discount)
                            )
                        )
                        subtotal += price_aux
                        total += (
                            price_aux + (price_aux * l.product.vat.tax)
                        )
                    else:
                        subtotal += l.quantity * l.price_sold
                        total += l.quantity * (
                            l.price_sold + (
                                l.price_sold * l.product.vat.tax
                            )
                        )

                instance.subtotal = subtotal
                instance.total = total

            instance.save()

        return instance
