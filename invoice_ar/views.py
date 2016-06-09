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
        queryset = models.InvoiceAR.objects.filter(concept_type=pk)

        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        if year is not None:
            queryset = queryset.filter(invoice_date__year=year)
        if month is not None:
            queryset = queryset.filter(invoice_date__month=month)

        return queryset


class InvoicesByContactList(ListAPIView):
    serializer_class = serializers.InvoiceARSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = models.InvoiceAR.objects.filter(invoicear_contact=pk)

        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        if year is not None:
            queryset = queryset.filter(invoice_date__year=year)
        if month is not None:
            queryset = queryset.filter(invoice_date__month=month)

        return queryset


class InvoicesByCompanyList(ListAPIView):
    serializer_class = serializers.InvoiceARSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = models.InvoiceAR.objects.filter(invoicear_company=pk)

        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        if year is not None:
            queryset = queryset.filter(invoice_date__year=year)
        if month is not None:
            queryset = queryset.filter(invoice_date__month=month)

        return queryset


class InvoiceARViewSet(ModelViewSet):
    queryset = models.InvoiceAR.objects.all()
    serializer_class = serializers.InvoiceARSerializer


class InvoiceARHasVATSubtotalViewSet(ModelViewSet):
    queryset = models.InvoiceARHasVATSubtotal.objects.all()
    serializer_class = serializers.InvoiceARHasVATSubtotalSerializer
