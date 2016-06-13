from django.db import transaction

from rest_framework.decorators import detail_route
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from accounting.models import Transaction, Account
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
        return models.InvoiceLine.objects.filter(product=pk)


class InvoiceTypeViewSet(ModelViewSet):
    queryset = models.InvoiceType.objects.all()
    serializer_class = serializers.InvoiceTypeSerializer


class InvoiceViewSet(ModelViewSet):
    queryset = models.Invoice.objects.all()
    serializer_class = serializers.InvoiceSerializer

    @detail_route(methods=['post'])
    @transaction.atomic
    def accept(self, request, pk=None):
        invoice = models.Invoice.objects.get(pk=pk) 
        if invoice.status == models.INVOICE_STATUSTYPE_DRAFT:
            debit_account = invoice.invoice_debit_account
            credit_account = invoice.invoice_credit_account
            transaction = Transaction.objects.create(
                amount=invoice.total,
                debit_account=debit_account,
                debit_account_balance=debit_account.balance-invoice.total,
                credit_account=credit_account,
                credit_account_balance=credit_account.balance+invoice.total,
            )
            invoice.transaction = transaction
            invoice.status = models.INVOICE_STATUSTYPE_ACCEPTED
            invoice.save()

    @detail_route(methods=['post'])
    @transaction.atomic
    def send(self, request, pk=None):
        invoice = models.Invoice.objects.get(pk=pk) 
        if invoice.status == models.INVOICE_STATUSTYPE_ACCEPTED:
            invoice.status = models.INVOICE_STATUSTYPE_SENT
            invoice.save()


class InvoicesByInvoiceTypeList(ListAPIView):
    serializer_class = serializers.InvoiceSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = models.Invoice.objects.filter(invoice_type=pk)

        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        if year is not None:
            queryset = queryset.filter(invoice_date__year=year)
        if month is not None:
            queryset = queryset.filter(invoice_date__month=month)

        return queryset


class InvoicesByCompanyList(ListAPIView):
    serializer_class = serializers.InvoiceSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = models.Invoice.objects.filter(invoice_company=pk)

        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        if year is not None:
            queryset = queryset.filter(invoice_date__year=year)
        if month is not None:
            queryset = queryset.filter(invoice_date__month=month)

        return queryset


class InvoicesByContactList(ListAPIView):
    serializer_class = serializers.InvoiceSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = models.Invoice.objects.filter(invoice_contact=pk)

        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        if year is not None:
            queryset = queryset.filter(invoice_date__year=year)
        if month is not None:
            queryset = queryset.filter(invoice_date__month=month)

        return queryset
