from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from persons.models import Company
from accounting import models


class LedgerTestCase(APITestCase):
    """
    """
    fixtures = [
        'accounting/tests/fixtures/users.json',
        'accounting/tests/fixtures/companies.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:accounting:ledger-list')
        data = {
            'persons_company': (
                reverse(
                    'api:persons:company-detail',
                    args=[Company.objects.get(fantasy_name='IRONA').pk]
                )
            ),
            'name': 'Do Easy'
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.Ledger.objects.get().delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Ledger.objects.count(), 1)

    def test_correctness(self):
        obj = models.Ledger.objects.get(name='Do Easy')
        self.assertEqual(
            obj.persons_company,
            Company.objects.get(fantasy_name='IRONA')
        )
        self.assertEqual(
            obj.name,
            'Do Easy'
        )


class AccountTestCase(APITestCase):
    """
    """
    fixtures = [
        'accounting/tests/fixtures/users.json',
        'accounting/tests/fixtures/companies.json',
        'accounting/tests/fixtures/accounts.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:accounting:account-list')
        data = {
            'ledger': (
                reverse(
                    'api:accounting:ledger-detail',
                    args=[models.Ledger.objects.get(name='Do Easy').pk]
                )
            ),
            'account_type': None,
            'code': '1',
            'name': 'Do Easy',
            'balance': Decimal('0.00')
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.Account.objects.get(code='1').delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Account.objects.count(), 3)

    def test_correctness(self):
        obj = models.Account.objects.get(code='1')
        self.assertEqual(
            obj.ledger,
            models.Ledger.objects.get(name='Do Easy')
        )
        self.assertEqual(
            obj.account_type,
            None
        )
        self.assertEqual(
            obj.code,
            '1'
        )
        self.assertEqual(
            obj.name,
            'Do Easy'
        )
        self.assertEqual(
            obj.balance,
            Decimal('0.00')
        )


class TransactionTestCase(APITestCase):
    """
    """
    fixtures = [
        'accounting/tests/fixtures/users.json',
        'accounting/tests/fixtures/companies.json',
        'accounting/tests/fixtures/accounts.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:accounting:account-list')
        data = {
            'amount': Decimal('100.00'),
            'debit_account': (
                reverse(
                    'api:accounting:account-detail',
                    args=[models.Account.objects.get(name='Do Easy').pk]
                )
            ),
            'debit_account_balance': Decimal('100.00'),
            'credit_account': (
                reverse(
                    'api:accounting:account-detail',
                    args=[models.Account.objects.get(name='Do No Easy').pk]
                )
            ),
            'credit_account_balance': Decimal('100.00'),
        }
        self.response = self.client.post(url, data)

    def test_create(self):
        self.assertEqual(
            self.response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(models.Transaction.objects.count(), 0)


class CompanyAccountingTestCase(APITestCase):
    """
    """
    fixtures = [
        'accounting/tests/fixtures/users.json',
        'accounting/tests/fixtures/companies.json',
        'accounting/tests/fixtures/accounts.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:accounting:companyaccounting-list')
        do_easy_account = models.Account.objects.get(name='Do Easy')
        do_no_easy_account = models.Account.objects.get(name='Do No Easy')
        data = {
            'persons_company': (
                reverse(
                    'api:persons:company-detail',
                    args=[Company.objects.get(fantasy_name='IRONA').pk]
                )
            ),
            'default_debit_account_for_cash': reverse(
                    'api:accounting:account-detail',
                    args=[do_easy_account.pk]
            ),
            'default_credit_account_for_cash': reverse(
                    'api:accounting:account-detail',
                    args=[do_no_easy_account.pk]
            ),
            'default_debit_account_for_creditcard': reverse(
                    'api:accounting:account-detail',
                    args=[do_easy_account.pk]
            ),
            'default_credit_account_for_creditcard': reverse(
                    'api:accounting:account-detail',
                    args=[do_no_easy_account.pk]
            ),
            'default_debit_account_for_debitcard': reverse(
                    'api:accounting:account-detail',
                    args=[do_easy_account.pk]
            ),
            'default_credit_account_for_debitcard': reverse(
                    'api:accounting:account-detail',
                    args=[do_no_easy_account.pk]
            ),
            'default_debit_account_for_bankaccount': reverse(
                    'api:accounting:account-detail',
                    args=[do_easy_account.pk]
            ),
            'default_credit_account_for_bankaccount': reverse(
                    'api:accounting:account-detail',
                    args=[do_no_easy_account.pk]
            ),
            'default_debit_account_for_check': reverse(
                    'api:accounting:account-detail',
                    args=[do_easy_account.pk]
            ),
            'default_credit_account_for_check': reverse(
                    'api:accounting:account-detail',
                    args=[do_no_easy_account.pk]
            ),
            'default_debit_account_for_paypal': reverse(
                    'api:accounting:account-detail',
                    args=[do_easy_account.pk]
            ),
            'default_credit_account_for_paypal': reverse(
                    'api:accounting:account-detail',
                    args=[do_no_easy_account.pk]
            ),
            'default_debit_account_for_googlewallet': reverse(
                    'api:accounting:account-detail',
                    args=[do_easy_account.pk]
            ),
            'default_credit_account_for_googlewallet': reverse(
                    'api:accounting:account-detail',
                    args=[do_no_easy_account.pk]
            ),
            'default_debit_account_for_applepay': reverse(
                    'api:accounting:account-detail',
                    args=[do_easy_account.pk]
            ),
            'default_credit_account_for_applepay': reverse(
                    'api:accounting:account-detail',
                    args=[do_no_easy_account.pk]
            ),
            'default_debit_account_for_bitcoin': reverse(
                    'api:accounting:account-detail',
                    args=[do_easy_account.pk]
            ),
            'default_credit_account_for_bitcoin': reverse(
                    'api:accounting:account-detail',
                    args=[do_no_easy_account.pk]
            )
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.CompanyAccounting.objects.get().delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.CompanyAccounting.objects.count(), 1)

    def test_correctness(self):
        obj = models.CompanyAccounting.objects.get(
            persons_company__fantasy_name='IRONA'
        )
        do_easy_account = models.Account.objects.get(name='Do Easy')
        do_no_easy_account = models.Account.objects.get(name='Do No Easy')
        self.assertEqual(
            obj.persons_company,
            Company.objects.get(fantasy_name='IRONA')
        )
        self.assertEqual(
            obj.default_debit_account_for_cash,
            do_easy_account
        )
        self.assertEqual(
            obj.default_credit_account_for_cash,
            do_no_easy_account
        )
        self.assertEqual(
            obj.default_debit_account_for_creditcard,
            do_easy_account
        )
        self.assertEqual(
            obj.default_credit_account_for_creditcard,
            do_no_easy_account
        )
        self.assertEqual(
            obj.default_debit_account_for_debitcard,
            do_easy_account
        )
        self.assertEqual(
            obj.default_credit_account_for_debitcard,
            do_no_easy_account
        )
        self.assertEqual(
            obj.default_debit_account_for_bankaccount,
            do_easy_account
        )
        self.assertEqual(
            obj.default_credit_account_for_bankaccount,
            do_no_easy_account
        )
        self.assertEqual(
            obj.default_debit_account_for_check,
            do_easy_account
        )
        self.assertEqual(
            obj.default_credit_account_for_check,
            do_no_easy_account
        )
        self.assertEqual(
            obj.default_debit_account_for_paypal,
            do_easy_account
        )
        self.assertEqual(
            obj.default_credit_account_for_paypal,
            do_no_easy_account
        )
        self.assertEqual(
            obj.default_debit_account_for_googlewallet,
            do_easy_account
        )
        self.assertEqual(
            obj.default_credit_account_for_googlewallet,
            do_no_easy_account
        )
        self.assertEqual(
            obj.default_debit_account_for_applepay,
            do_easy_account
        )
        self.assertEqual(
            obj.default_credit_account_for_applepay,
            do_no_easy_account
        )
        self.assertEqual(
            obj.default_debit_account_for_bitcoin,
            do_easy_account
        )
        self.assertEqual(
            obj.default_credit_account_for_bitcoin,
            do_no_easy_account
        )
