from rest_framework.serializers import HyperlinkedModelSerializer

from accounting import models


class LedgerSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.Ledger
        fields = (
            'url',
            'id',
            'company',
            'name'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:accounting:ledger-detail'
            },
            'company': {
                'view_name': 'api:persons:company-detail'
            }
        }


class AccountSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.Account
        fields = (
            'url',
            'id',
            'ledger',
            'code',
            'name',
            'account_subtype',
            'balance'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:accounting:account-detail'
            },
            'ledger': {
                'view_name': 'api:accounting:ledger-detail'
            },
            'account_subtype': {
                'view_name': 'api:accounting:accountsubtype-detail'
            }
        }


class AccountSubtypeSerializer(HyperlinkedModelSerializer):
        class Meta:
            model = models.AccountSubtype
            fields = (
                'url',
                'id',
                'company',
                'main_type',
                'name'
            )
            extra_kwargs = {
                'url': {
                    'view_name': 'api:accounting:accountsubtype-detail'
                },
                'company': {
                    'view_name': 'api:persons:company-detail'
                }
            }


class TransactionSerializer(HyperlinkedModelSerializer):
        class Meta:
            model = models.Transaction
            read_only_fields = (
                'url',
                'id',
                'amount',
                'debit_account',
                'debit_account_balance',
                'credit_account',
                'credit_account_balance'
            )
            extra_kwargs = {
                'url': {
                    'view_name': 'api:accounting:transaction-detail'
                },
                'debit_account': {
                    'view_name': 'api:accounting:account-detail'
                },
                'credit_account': {
                    'view_name': 'api:accounting:account-detail'
                }
            }
