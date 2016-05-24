from rest_framework.serializers import HyperlinkedModelSerializer

from invoice.serializers import (CompanyInvoiceSerializer,
                                 ContactInvoiceSerializer)
from invoice_ar import models


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
                'view_name': 'api:invoice_ar:contactar-detail'
            }
        }


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
