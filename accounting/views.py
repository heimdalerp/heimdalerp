from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from accounting import models, serializers


class LedgerViewSet(ModelViewSet):
    queryset = models.Ledger.objects.all()
    serializer_class = serializers.LedgerSerializer


class LedgersByCompanyList(ListAPIView):
    serializer_class = serializers.LedgerSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Ledger.objects.filter(company=pk)


class AccountViewSet(ModelViewSet):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer


class AccountsByLedgerList(ListAPIView):
    serializer_class = serializers.AccountSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Account.objects.filter(ledger=pk)


class TransactionViewSet(ReadOnlyModelViewSet):
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer


class TransactionsByAccountList(ListAPIView):
    serializer_class = serializers.TransactionSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Transaction.objects.filter(
            Q(debit_account=pk) | Q(credit_account=pk)
        )


class PaymentViewSet(ModelViewSet):
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializer


class PaymentsByContactList(ListAPIView):
    serializer_class = serializers.PaymentSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = models.Payment.objects.filter(contact=pk)

        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')
        if year is not None:
            queryset = queryset.filter(invoice_date__year=year)
        if month is not None:
            queryset = queryset.filter(invoice_date__month=month)
        if day is not None:
            queryset = queryset.filter(invoice_date__day=day)

        return queryset


class PaymentsByCompanyList(ListAPIView):
    serializer_class = serializers.PaymentSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = models.Payment.objects.filter(contact__company=pk)

        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')
        if year is not None:
            queryset = queryset.filter(invoice_date__year=year)
        if month is not None:
            queryset = queryset.filter(invoice_date__month=month)
        if day is not None:
            queryset = queryset.filter(invoice_date__day=day)

        return queryset


class CompanyAccountingViewSet(ModelViewSet):
    queryset = models.CompanyAccounting.objects.all()
    serializer_class = serializers.CompanyAccountingSerializer
