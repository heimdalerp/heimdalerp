from django.db import transaction
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
            'account_type',
            'code',
            'name',
            'balance'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:accounting:account-detail'
            },
            'ledger': {
                'view_name': 'api:accounting:ledger-detail'
            },
            'balance': {
                'coerce_to_string': False
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
                },
                'amount': {
                    'coerce_to_string': False
                },
                'debit_account_balance': {
                    'coerce_to_string': False
                },
                'credit_account_balance': {
                    'coerce_to_string': False
                }
            }


class PaymentSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Payment
        fields = (
            'url',
            'id',
            'accounting_company',
            'contact_contact',
            'payment_date',
            'payment_type',
            'payment_method',
            'amount'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:accounting:payment-detail'
            },
            'contact_contact': {
                'view_name': 'api:contact:contact-detail'
            },
            'amount': {
                'coerce_to_string': False
            }
        }

    @transaction.atomic
    def create(self, validated_data):
        accounting_company = validated_data.get('accounting_company')
        payment_method = validated_data.get('payment_method')
        amount = validated_data.get('amount')

        if payment_method == models.PAYMENT_METHOD_CASH:
            debit_account = (
                accounting_company.default_debit_account_cash
            )
            credit_account = (
                accounting_company.default_credit_account_crash
            )
        elif payment_method == models.PAYMENT_METHOD_CREDITCARD:
            debit_account = (
                accounting_company.default_debit_account_creditcard
            )
            credit_account = (
                accounting_company.default_credit_account_creditcard
            )

        elif payment_method == models.PAYMENT_METHOD_DEBITCARD:
            debit_account = (
                accounting_company.default_debit_account_debitcard
            )
            credit_account = (
                accounting_company.default_credit_account_debitcard
            )

        elif payment_method == models.PAYMENT_METHOD_BANKACCOUNT:
            debit_account = (
                accounting_company.default_debit_account_bankaccount
            )
            credit_account = (
                accounting_company.default_credit_account_bankaccount
            )

        elif payment_method == models.PAYMENT_METHOD_CHECK:
            debit_account = (
                accounting_company.default_debit_account_check
            )
            credit_account = (
                accounting_company.default_credit_account_check
            )

        elif payment_method == models.PAYMENT_METHOD_PAYPAL:
            debit_account = (
                accounting_company.default_debit_account_paypal
            )
            credit_account = (
                accounting_company.default_credit_account_paypal
            )

        elif payment_method == models.PAYMENT_METHOD_GOOGLEWALLET:
            debit_account = (
                accounting_company.default_debit_account_googlewallet
            )
            credit_account = (
                accounting_company.default_credit_account_googlewallet
            )

        elif payment_method == models.PAYMENT_METHOD_APPLEPAY:
            debit_account = (
                accounting_company.default_debit_account_applepay
            )
            credit_account = (
                accounting_company.default_credit_account_applepay
            )

        elif payment_method == models.PAYMENT_METHOD_BITCOIN:
            debit_account = (
                accounting_company.default_debit_account_bitcoin
            )
            credit_account = (
                accounting_company.default_credit_account_bitcoin
            )

        transaction = models.Transaction.objects.create(
            amount=amount,
            debit_account=debit_account,
            debit_account_balance=debit_account.balance+amount,
            credit_account=credit_account,
            credit_account_balance=credit_account.balance+amount
        )

        validated_data['transaction'] = transaction
        return models.Payment.objects.create(**validated_data)


class CompanyAccountingSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.CompanyAccounting
        fields = (
            'url',
            'id',
            'persons_company',
            'default_debit_account_for_cash',
            'default_credit_account_for_cash',
            'default_debit_account_for_creditcard',
            'default_credit_account_for_creditcard',
            'default_debit_account_for_debitcard',
            'default_credit_account_for_debitcard',
            'default_debit_account_for_bankaccount',
            'default_credit_account_for_bankaccount',
            'default_debit_account_for_check',
            'default_credit_account_for_check',
            'default_debit_account_for_paypal',
            'default_credit_account_for_paypal',
            'default_debit_account_for_googlewallet',
            'default_credit_account_for_googlewallet',
            'default_debit_account_for_applepay',
            'default_credit_account_for_applepay',
            'default_debit_account_for_bitcoin',
            'default_credit_account_for_bitcoin'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:accounting:companyaccounting-detail'
            },
            'persons_company': {
                'view_name': 'api:persons:company-detail'
            },
            'default_debit_account_for_cash': {
                'view_name': 'api:accounting:account-detail'
            },
            'default_credit_account_for_cash': {
                'view_name': 'api:accounting:account-detail'
            },
            'default_debit_account_for_creditcard': {
                'view_name': 'api:accounting:account-detail'
            },
            'default_credit_account_for_creditcard': {
                'view_name': 'api:accounting:account-detail'
            },
            'default_debit_account_for_debitcard': {
                'view_name': 'api:accounting:account-detail'
            },
            'default_credit_account_for_debitcard': {
                'view_name': 'api:accounting:account-detail'
            },
            'default_debit_account_for_bankaccount': {
                'view_name': 'api:accounting:account-detail'
            },
            'default_credit_account_for_bankaccount': {
                'view_name': 'api:accounting:account-detail'
            },
            'default_debit_account_for_check': {
                'view_name': 'api:accounting:account-detail'
            },
            'default_credit_account_for_check': {
                'view_name': 'api:accounting:account-detail'
            },
            'default_debit_account_for_paypal': {
                'view_name': 'api:accounting:account-detail'
            },
            'default_credit_account_for_paypal': {
                'view_name': 'api:accounting:account-detail'
            },
            'default_debit_account_for_googlewallet': {
                'view_name': 'api:accounting:account-detail'
            },
            'default_credit_account_for_googlewallet': {
                'view_name': 'api:accounting:account-detail'
            },
            'default_debit_account_for_applepay': {
                'view_name': 'api:accounting:account-detail'
            },
            'default_credit_account_for_applepay': {
                'view_name': 'api:accounting:account-detail'
            },
            'default_debit_account_for_bitcoin': {
                'view_name': 'api:accounting:account-detail'
            },
            'default_credit_account_for_bitcoin': {
                'view_name': 'api:accounting:account-detail'
            }
        }
