from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from contact.models import Contact
from invoice import models, serializers


class FiscalPositionViewSet(ModelViewSet):
    queryset = models.FiscalPosition.objects.all()
    serializer_class = serializers.FiscalPositionSerializer


class CompanyInvoiceViewSet(ModelViewSet):
    queryset = models.CompanyInvoice.objects.all()
    serializer_class = serializers.CompanyInvoiceSerializer


class ContactInvoiceViewSet(ModelViewSet):
    queryset = models.ContactInvoice.objects.all()
    serializer_class = serializers.ContactInvoiceSerializer


class ContactsByCompanyList(ListAPIView):
    serializer_class = serializers.ContactInvoiceSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        company = models.CompanyInvoice.objects.filter(pk=pk)
        return company.contacts.all()


class CompaniesByFiscalPositionList(ListAPIView):
    serializer_class = serializers.CompanyInvoiceSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        fiscal_position = models.FiscalPosition.objects.filter(pk=pk)
        return fiscal_position.companies.all()


class ContactsByFiscalPositionList(ListAPIView):
    serializer_class = serializers.ContactInvoiceSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        fiscal_position = models.FiscalPosition.objects.filter(pk=pk)
        return fiscal_position.contacts.all()


class VATViewSet(ModelViewSet):
    queryset = models.VAT.objects.all()
    serializer_class = serializers.VATSerializer


class ProductViewSet(ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class ProductsByCompanyList(ListAPIView):
    serializer_class = serializers.ProductSerializer

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
    serializer_class = serializers.InvoiceLineSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        product = models.Product.objects.filter(pk=pk)
        return product.invoice_lines.all()


class InvoiceViewSet(ModelViewSet):
    queryset = models.Invoice.objects.all()
    serializer_class = serializers.InvoiceSerializer


class InvoicesByCompanyList(ListAPIView):
    serializer_class = serializers.InvoiceSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        company = models.CompanyInvoice.objects.filter(pk=pk)
        return company.invoices.all()


class InvoicesByContactList(ListAPIView):
    serializer_class = serializers.InvoiceSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        contact = Contact.objects.filter(pk=pk)
        return contact.invoices.all()
