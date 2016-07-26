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
        self.assertEqual(models.Ledger.objects.count(), 1)

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
