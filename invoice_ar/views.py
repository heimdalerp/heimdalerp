from rest_framework.viewsets import ModelViewSet

from invoice_ar import models, serializers


class ClientARViewSet(ModelViewSet):
    queryset = models.ClientAR.objects.all()
    serializer_class = serializers.ClientARSerializer


class CompanyInvoiceARViewSet(ModelViewSet):
    queryset = models.CompanyInvoiceAR.objects.all()
    serializer_class = serializers.CompanyInvoiceARSerializer
