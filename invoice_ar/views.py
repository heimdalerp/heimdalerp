from rest_framework.generics import ListAPIView
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


class ConceptTypeViewSet(ModelViewSet):
    queryset = models.ConceptType.objects.all()
    serializer_class = serializers.ConceptTypeSerializer


class InvoicesByConceptTypeList(ListAPIView):
    serializer_class = serializers.InvoiceARSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.InvoiceAR.objects.filter(concept_type=pk)


class InvoiceARViewSet(ModelViewSet):
    queryset = models.InvoiceAR.objects.all()
    serializer_class = serializers.InvoiceARSerializer


class InvoiceARHasVATSubtotalViewSet(ModelViewSet):
    queryset = models.InvoiceARHasVATSubtotal.objects.all()
    serializer_class = serializers.InvoiceARHasVATSubtotalSerializer
