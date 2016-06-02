from rest_framework.viewsets import ModelViewSet

from invoice_ar import models, serializers


class ContactInvoiceARViewSet(ModelViewSet):
    queryset = models.ContactInvoiceAR.objects.all()
    serializer_class = serializers.ContactInvoiceARSerializer


class CompanyInvoiceARViewSet(ModelViewSet):
    queryset = models.CompanyInvoiceAR.objects.all()
    serializer_class = serializers.CompanyInvoiceARSerializer


class PointOfSaleViewSet(ModelViewSet):
    queryset = models.PointOfSale.objects.all()
    serializer_class = serializers.PointOfSaleSerializer


class InvoiceTypeViewSet(ModelViewSet):
    queryset = models.InvoiceType.objects.all()
    serializer_class = serializers.InvoiceTypeSerializer


class InvoiceARViewSet(ModelViewSet):
    queryset = models.InvoiceAR.objects.all()
    serializer_class = serializers.InvoiceARSerializer


class InvoiceARHasVATSubtotalViewSet(ModelViewSet):
    queryset = models.InvoiceARHasVATSubtotalViewSet.objects.all()
    serializer_class = serializers.InvoiceARHasVATSubtotalSerializer
