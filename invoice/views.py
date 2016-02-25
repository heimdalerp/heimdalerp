from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from invoice import models, serializers


class FiscalPositionViewSet(ModelViewSet):
    queryset = models.FiscalPosition.objects.all()
    serializer_class = serializers.FiscalPositionSerializer


class CompanyViewSet(ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer


class CompaniesByFiscalPositionList(ListAPIView):
    serializer_class = serializers.FiscalPositionSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        fiscal_position = models.FiscalPosition.objects.filter(pk=pk)
        return fiscal_position.companies.all() 


class CompaniesByClientList(ListAPIView):
    serializer_class = serializers.ClientSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        client = models.Client.objects.filter(pk=pk)
        return client.companies.all() 


class ClientViewSet(ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.ClientSerializer


class ClientsByFiscalPositionList(ListAPIView):
    serializer_class = serializers.FiscalPositionSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        fiscal_position = models.FiscalPosition.objects.filter(pk=pk)
        return fiscal_position.clients.all() 


class ClientsByCompanyList(ListAPIView):
    serializer_class = serializers.CompanyInvoiceSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        company = models.CompanyInvoice.objects.filter(pk=pk)
        return company.clients.all() 


class VATViewSet(ModelViewSet):
    queryset = models.VAT.objects.all()
    serializer_class = serializers.VATSerializer


class InvoiceProductViewSet(ModelViewSet):
    queryset = models.InvoiceProduct.objects.all()
    serializer_class = serializers.InvoiceProductSerializer


class ProductsByCompanyList(ListAPIView):
    serializer_class = serializers.CompanyInvoiceSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        company = models.CompanyInvoice.objects.filter(pk=pk)
        return company.products.all() 


class ProductsByVATList(ListAPIView):
    serializer_class = serializers.VATSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        vat = models.VAT.objects.filter(pk=pk)
        return vat.products.all() 


class InvoiceLineViewSet(ModelViewSet):
    queryset = models.InvoiceLine.objects.all()
    serializer_class = serializers.InvoiceLineSerializer


class InvoiceLinesByProductList(ListAPIView):
    serializer_class = serializers.InvoiceProductSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        product = models.InvoiceProduct.objects.filter(pk=pk)
        return product.invoice_lines.all() 


class InvoiceViewSet(ModelViewSet):
    queryset = models.Invoice.objects.all()
    serializer_class = serializers.InvoiceSerializer


class InvoicesByCompanyList(ListAPIView):
    serializer_class = serializers.CompanyInvoiceSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        company = models.CompanyInvoice.objects.filter(pk=pk)
        return company.invoices.all() 


class InvoicesByClientList(ListAPIView):
    serializer_class = serializers.ClientSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        client = models.Client.objects.filter(pk=pk)
        return client.invoices.all() 

