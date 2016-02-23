from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from invoice import models, serializers


class FiscalPositionViewSet(ModelViewSet):
    queryset = models.FiscalPosition.objects.all()
    serializer_class = serializers.FiscalPositionSerializer


class CompanyViewSet(ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer


class ClientViewSet(ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.ClientSerializer


class VATViewSet(ModelViewSet):
    queryset = models.VAT.objects.all()
    serializer_class = serializers.VATSerializer


class InvoiceProductViewSet(ModelViewSet):
    queryset = models.InvoiceProduct.objects.all()
    serializer_class = serializers.InvoiceProductSerializer


class InvoiceLineViewSet(ModelViewSet):
    queryset = models.InvoiceLine.objects.all()
    serializer_class = serializers.InvoiceLineSerializer


class InvoiceViewSet(ModelViewSet):
    queryset = models.Invoice.objects.all()
    serializer_class = serializers.InvoiceSerializer

