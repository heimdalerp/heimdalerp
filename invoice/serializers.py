from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.serializers import HyperlinkedIdentityField

from invoice import models
from persons.serializers import PhoneNumberSerializer
from persons.serializers import ExtraEmailAddressSerializer
from persons.serializers import PhysicalAddressSerializer


class FiscalPositionSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.FiscalPosition


class CompanySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Company


class ClientSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Client


class VAT(HyperlinkedModelSerializer):

    class Meta:
        model = models.VAT


class InvoiceProduct(HyperlinkedModelSerializer):

    class Meta:
        model = models.InvoiceProduct


class InvoiceLine(HyperlinkedModelSerializer):

    class Meta:
        model = models.InvoiceLine


class Invoice(HyperlinkedModelSerializer):

    class Meta:
        model = models.Invoice


