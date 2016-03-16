from django.db.models import Q

from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

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


class AccountsByAccountSubtypeList(ListAPIView):
    serializer_class = serializers.AccountSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Account.objects.filter(account_subtype=pk)


class AccountSubtypeViewSet(ModelViewSet):
    queryset = models.AccountSubtype.objects.all()
    serializer_class = serializers.AccountSubtypeSerializer


class AccountSubtypesByCompanyList(ListAPIView):
    serializer_class = serializers.AccountSubtypeSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.AccountSubtype.objects.filter(company=pk)


# TODO: Perhaps this should be a read-only serializer.
class TransactionViewSet(ModelViewSet):
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer


class TransactionsByAccountList(ListAPIView):
    serializer_class = serializers.TransactionSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Transaction.objects.filter(
            Q(debit_account) | Q(credit_account)
        )
