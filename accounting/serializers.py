from rest_framework.serializers import HyperlinkedModelSerializer

from accounting import models


class LedgerSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Ledger
        fields = (
            'url',
            'id',
            'persons_company',
            'name'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:accounting:ledger-detail'
            },
            'persons_company': {
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


class PaymentSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Payment
        fields = (
            'url',
            'id',
            'contact_contact',
            'account',
            'amount'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:accounting:payment-detail'
            },
            'contact_contact': {
                'view_name': 'api:contact:contact-detail'
            },
            'account': {
                'view_name': 'api:accounting:account-detail'
            }
        }
