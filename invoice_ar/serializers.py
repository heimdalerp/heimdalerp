from decimal import Decimal

from contact.models import Contact
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from invoice.models import (INVOICE_STATUSTYPE_DRAFT, VAT, CompanyInvoice,
                            ContactInvoice, InvoiceLine)
from invoice.serializers import (CompanyInvoiceSerializer,
                                 ContactInvoiceSerializer,
                                 InvoiceLineSerializer)
from invoice_ar import models
from persons.models import Company, PhysicalAddress
from persons.serializers import PhysicalAddressSerializer
from rest_framework.serializers import (HyperlinkedIdentityField,
                                        HyperlinkedModelSerializer,
                                        ValidationError)


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

    @transaction.atomic
    def create(self, validated_data):  # TODO: Use existing objects.
        id_type = validated_data.get('id_type')
        id_number = validated_data.get('id_number')
        if id_type is None or id_number is None:
            raise ValidationError(_("ID type or ID number not sent."))
        id_number = id_number.replace('.', '')
        id_number = id_number.replace(' ', '')
        id_number = id_number.replace('-', '')
        if id_type == models.ID_TYPE_DNI:
            if len(id_number) != 8 or not id_number.isdigit():
                raise ValidationError(_("A DNI must be 8 numbers long."))
        else:
            if len(id_number) == 11 and id_number.isdigit():
                base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
                aux = 0
                for i in range(10):
                    aux += int(id_number[i]) * base[i]
                aux = 11 - (aux % 11)
                if aux == 11:
                    aux = 0
                if int(id_number[10]) != aux:
                    raise ValidationError(
                        _("The number entered isn't a valid CUIT/CUIL.")
                    )
            else:
                raise ValidationError(
                    _("A CUIT/CUIL must be 11 numbers long.")
                )
        validated_data['id_number'] = id_number

        invoice_contact_data = validated_data['invoice_contact']
        contact_contact_data = invoice_contact_data.pop('contact_contact')
        home_address_data = contact_contact_data.pop('home_address')
        home_address = PhysicalAddress.objects.create(
            **home_address_data
        )
        contact_contact_data['home_address'] = home_address

        contact_contact = Contact.objects.create(
            **contact_contact_data
        )
        invoice_contact_data['contact_contact'] = contact_contact

        fiscal_address_data = invoice_contact_data.pop('fiscal_address')
        fiscal_address = PhysicalAddress.objects.create(
            **fiscal_address_data
        )
        invoice_contact_data['fiscal_address'] = fiscal_address
        invoice_contact = ContactInvoice.objects.create(
            **invoice_contact_data
        )
        validated_data['invoice_contact'] = invoice_contact

        invoicear_contact = models.ContactInvoiceAR.objects.create(
            **validated_data
        )
        return invoicear_contact

    @transaction.atomic
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
        contact_contact.home_address.locality = (
            home_address_data.get(
                'locality',
                contact_contact.home_address.locality
            )
        )
        contact_contact.home_address.postal_code = (
            home_address_data.get(
                'postal_code',
                contact_contact.home_address.postal_code
            )
        )
        contact_contact.home_address.save()

        contact_contact.persons_company = contact_contact_data.get(
            'persons_company',
            contact_contact.persons_company
        )
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
        invoice_contact.fiscal_address.locality = (
            fiscal_address_data.get(
                'locality',
                invoice_contact.fiscal_address.locality
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
            'id_number',
            instance.id_number
        )

        instance.save()
        return instance


class CompanyInvoiceARSerializer(HyperlinkedModelSerializer):
    invoice_company = CompanyInvoiceSerializer()
    invoices = HyperlinkedIdentityField(
        view_name='api:invoice_ar:companyinvoicear-invoices'
    )
    webservice_sessions = HyperlinkedIdentityField(
        view_name='api:invoice_ar:companyinvoicear-webservicesessions'
    )

    class Meta:
        model = models.CompanyInvoiceAR
        fields = (
            'url',
            'id',
            'invoice_company',
            'cuit',
            'iibb',
            'key',
            'cert',
            'invoices',
            'webservice_sessions'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice_ar:companyinvoicear-detail'
            }
        }

    @transaction.atomic
    def create(self, validated_data):  # TODO: Use existing objects.
        invoice_company_data = validated_data.pop('invoice_company')
        persons_company_data = invoice_company_data.pop('persons_company')
        persons_company = Company.objects.create(
            **persons_company_data
        )
        invoice_company_data['persons_company'] = persons_company

        fiscal_address_data = invoice_company_data.pop('fiscal_address')
        fiscal_address = PhysicalAddress.objects.create(
            **fiscal_address_data
        )
        invoice_company_data['fiscal_address'] = fiscal_address

        invoice_company = CompanyInvoice.objects.create(
            **invoice_company_data
        )
        validated_data['invoice_company'] = invoice_company

        company = models.CompanyInvoiceAR.objects.create(**validated_data)
        return company

    @transaction.atomic
    def update(self, instance, validated_data):
        invoice_company_data = validated_data.pop('invoice_company')
        persons_company_data = invoice_company_data.pop('persons_company')

        invoice_company = instance.invoice_company
        persons_company = instance.invoice_company.persons_company

        persons_company.fantasy_name = persons_company_data.get(
            'fantasy_name',
            persons_company.fantasy_name
        )
        persons_company.slogan = persons_company_data.get(
            'slogan',
            persons_company.slogan
        )

        persons_company.save()

        invoice_company.legal_name = invoice_company_data.get(
            'legal_name',
            invoice_company.legal_name
        )
        invoice_company.initiated_activities = (
            invoice_company_data.get(
                'initiated_activities',
                invoice_company.initiated_activities
            )
        )
        invoice_company.fiscal_position = invoice_company_data.get(
            'fiscal_position',
            invoice_company.fiscal_position
        )

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
        invoice_company.fiscal_address.locality = (
            fiscal_address_data.get(
                'locality',
                invoice_company.fiscal_address.locality
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


class WebServiceSessionSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.WebServiceSession
        fields = (
            'url',
            'id',
            'invoicear_company',
            'generation',
            'expiration',
            'token',
            'sign'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice_ar:webservicesession-detail'
            },
            'invoicear_company': {
                'view_name': 'api:invoice_ar:companyinvoicear-detail'
            }
        }


class PointOfSaleARSerializer(HyperlinkedModelSerializer):
    fiscal_address = PhysicalAddressSerializer()
    invoices = HyperlinkedIdentityField(
        view_name='api:invoice_ar:pointofsalear-invoices'
    )

    class Meta:
        model = models.PointOfSaleAR
        fields = (
            'url',
            'id',
            'invoicear_company',
            'afip_id',
            'fantasy_name',
            'point_of_sale_type',
            'fiscal_address',
            'is_inactive',
            'invoices'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice_ar:pointofsalear-detail'
            },
            'invoicear_company': {
                'view_name': 'api:invoice_ar:companyinvoicear-detail'
            }
        }

    @transaction.atomic
    def create(self, validated_data):
        fiscal_address_data = validated_data.pop('fiscal_address')
        fiscal_address = PhysicalAddress.objects.create(
            **fiscal_address_data
        )
        validated_data['fiscal_address'] = fiscal_address

        return models.PointOfSaleAR.objects.create(**validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.afip_id = validated_data.get(
            'afip_id',
            instance.afip_id
        )
        instance.fantasy_name = validated_data.get(
            'fantasy_name',
            instance.fantasy_name
        )
        instance.point_of_sale_type = validated_data.get(
            'point_of_sale_type',
            instance.point_of_sale_type
        )
        instance.is_inactive = validated_data.get(
            'is_inactive',
            instance.is_inactive
        )

        fiscal_address_data = validated_data.get('fiscal_address')
        if fiscal_address_data is not None:
            instance.fiscal_address.street_address = fiscal_address_data.get(
                'street_address',
                instance.fiscal_address.street_address
            )
            instance.fiscal_address.floor_number = fiscal_address_data.get(
                'floor_number',
                instance.fiscal_address.floor_number
            )
            instance.fiscal_address.apartment_number = fiscal_address_data.get(
                'apartment_number',
                instance.fiscal_address.apartment_number
            )
            instance.fiscal_address.locality = fiscal_address_data.get(
                'locality',
                instance.fiscal_address.locality
            )
            instance.fiscal_address.postal_code = fiscal_address_data.get(
                'postal_code',
                instance.fiscal_address.postal_code
            )
            instance.fiscal_address.save()

        instance.save()
        return instance


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
            },
            'subtotal': {
                'coerce_to_string': False
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
    vat_subtotals = InvoiceARHasVATSubtotalSerializer(
        many=True,
        read_only=True
    )

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
            'point_of_sale_ar',
            'due_date',
            'service_start',
            'service_end',
            'concept_type',
            'vat_total',
            'vat_subtotals'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice_ar:invoicear-detail'
            },
            'invoicear_company': {
                'view_name': 'api:invoice_ar:companyinvoicear-detail',
                'read_only': True
            },
            'invoice_type': {
                'view_name': 'api:invoice:invoicetype-detail'
            },
            'invoicear_contact': {
                'view_name': 'api:invoice_ar:contactinvoicear-detail'
            },
            'status': {
                'read_only': True
            },
            'subtotal': {
                'read_only': True,
                'coerce_to_string': False
            },
            'total': {
                'read_only': True,
                'coerce_to_string': False
            },
            'transaction': {
                'view_name': 'api:accounting:transaction-detail',
                'read_only': True
            },
            'point_of_sale_ar': {
                'view_name': 'api:invoice_ar:pointofsalear-detail'
            },
            'concept_type': {
                'view_name': 'api:invoice_ar:concepttype-detail'
            },
            'vat_total': {
                'read_only': True,
                'coerce_to_string': False
            }
        }

    @transaction.atomic
    def create(self, validated_data):
        validated_data['invoicear_company'] = (
            validated_data.get('point_of_sale_ar').invoicear_company
        )
        validated_data['invoice_company'] = (
            validated_data.get('invoicear_company').invoice_company
        )
        validated_data['invoice_contact'] = (
            validated_data.get('invoicear_contact').invoice_contact
        )

        validated_data['status'] = INVOICE_STATUSTYPE_DRAFT
        number = validated_data.get('number')
        if number is None or number == 0:
            validated_data['number'] = 0

        invoice_lines_data = validated_data.pop('invoice_lines')

        invoicear = models.InvoiceAR.objects.create(
            **validated_data
        )

        if invoice_lines_data is not None:
            subtotal = Decimal('0.00')
            total = Decimal('0.00')
            vat_total = Decimal('0.00')
            vat_subtotals_data = dict()
            for l_data in invoice_lines_data:
                l = InvoiceLine.objects.create(**l_data)
                if str(l.product.vat.id) not in vat_subtotals_data:
                    vat_subtotals_data[str(l.product.vat.id)] = (
                        Decimal(0.00)
                    )
                if l.discount > 0.00:
                    price_aux = Decimal(
                        l.quantity * (
                            l.price_sold - (l.price_sold * l.discount)
                        )
                    )
                    vat_aux = Decimal(price_aux * l.product.vat.tax)
                    subtotal += price_aux
                    total += price_aux + vat_aux
                    vat_total += vat_aux
                    vat_subtotals_data[str(l.product.vat.id)] += (
                        Decimal(vat_aux)
                    )
                else:
                    subtotal += l.price_sold * l.quantity
                    vat_aux = l.price_sold * l.product.vat.tax
                    total += l.quantity * (
                        l.price_sold + (l.price_sold * l.product.vat.tax)
                    )
                    vat_total += l.quantity * vat_aux
                    vat_subtotals_data[str(l.product.vat.id)] += (
                        Decimal(l.quantity * vat_aux)
                    )

                invoicear.invoice_lines.add(l)

            for key, value in vat_subtotals_data.items():
                vat = VAT.objects.get(pk=key)
                vatsubtotal = models.InvoiceARHasVATSubtotal.objects.create(
                    vat=vat,
                    subtotal=value
                )
                invoicear.vat_subtotals.add(vatsubtotal)

            invoicear.subtotal = subtotal
            invoicear.total = total
            invoicear.vat_total = vat_total
            invoicear.save()

        return invoicear

    @transaction.atomic
    def update(self, instance, validated_data):
        if instance.status is INVOICE_STATUSTYPE_DRAFT:
            instance.invoicear_company = validated_data.get(
                'invoicear_company',
                instance.invoicear_company
            )
            instance.invoicear_contact = validated_data.get(
                'invoicear_contact',
                instance.invoicear_contact
            )
            instance.number = validated_data.get(
                'number',
                instance.number
            )
            instance.invoice_type = validated_data.get(
                'invoice_type',
                instance.invoice_type
            )
            instance.invoice_date = validated_data.get(
                'invoice_date',
                instance.invoice_date
            )
            instance.notes = validated_data.get(
                'notes',
                instance.notes
            )
            instance.due_date = validated_data.get(
                'due_date',
                instance.due_date
            )
            instance.service_start = validated_data.get(
                'service_start',
                instance.service_start
            )
            instance.service_end = validated_data.get(
                'service_end',
                instance.service_end
            )
            instance.concept_type = validated_data.get(
                'concept_type',
                instance.concept_type
            )
            instance.point_of_sale_ar = validated_data.get(
                'point_of_sale_ar',
                instance.point_of_sale_ar
            )

            invoice_lines_data = validated_data.get('invoice_lines')
            if invoice_lines_data is not None:
                instance.invoice_lines.clear()
                subtotal = Decimal('0.00')
                total = Decimal('0.00')
                vat_total = Decimal('0.00')
                vat_subtotals_data = dict()
                for l_data in invoice_lines_data:
                    l = InvoiceLine.objects.create(**l_data)
                    instance.invoice_lines.add(l)
                    if str(l.product.vat.id) not in vat_subtotals_data:
                        vat_subtotals_data[str(l.product.vat.id)] = (
                            Decimal(0.00)
                        )
                    if l.discount > 0.00:
                        price_aux = Decimal(
                            l.quantity * (
                                l.price_sold - (l.price_sold * l.discount)
                            )
                        )
                        vat_aux = Decimal(price_aux * l.product.vat.tax)
                        subtotal += price_aux
                        total += price_aux + vat_aux
                        vat_total += price_aux * l.product.vat.tax
                        vat_subtotals_data[str(l.product.vat.id)] += (
                            vat_aux
                        )
                    else:
                        subtotal += l.quantity * l.price_sold
                        vat_aux = Decimal(l.price_sold * l.product.vat.tax)
                        total += l.quantity * (l.price_sold + vat_aux)
                        vat_total += l.quantity * vat_aux
                        vat_subtotals_data[str(l.product.vat.id)] += (
                            Decimal(l.quantity * vat_aux)
                        )

                instance.vat_subtotals.clear()
                for k, v in vat_subtotals_data.items():
                    vat = VAT.objects.get(pk=k)
                    vatsubtotal = (
                        models.InvoiceARHasVATSubtotal.objects.create(
                            vat=vat,
                            subtotal=v
                        )
                    )
                    instance.vat_subtotals.add(vatsubtotal)

                instance.subtotal = subtotal
                instance.total = total
                instance.vat_total = vat_total

            instance.save()

        return instance
