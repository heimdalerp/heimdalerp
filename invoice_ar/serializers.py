from rest_framework.serializers import HyperlinkedModelSerializer

from invoice.serializers import (ContactInvoiceSerializer,
                                 CompanyInvoiceSerializer)
from invoice_ar import models


class ContactInvoiceARSerializer(HyperlinkedModelSerializer):
    contact = ContactInvoiceSerializer()

    class Meta:
        model = models.ContactInvoiceAR
        fields = (
            'url',
            'id',
            'contact',
            'dni',
            'cuit',
            'cuil'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice_ar:contactar-detail'
            }
        }


class CompanyInvoiceARSerializer(HyperlinkedModelSerializer):
    company = CompanyInvoiceSerializer()

    class Meta:
        model = models.CompanyInvoiceAR
        fields = (
            'url',
            'id',
            'company',
            'cuit',
            'iibb'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:invoice_ar:companyinvoicear-detail'
            }
        }
