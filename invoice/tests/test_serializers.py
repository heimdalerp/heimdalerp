from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from geo.models import Locality, Country
from invoice import models


class CompanyInvoiceTestCase(APITestCase):
    """
    """
    fixtures = [
        'invoice/tests/fixtures/users.json',
        'invoice/tests/fixtures/geo.json',
        'invoice/tests/fixtures/invoicing.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:invoice:companyinvoice-list')
        data = {
            'persons_company': {
                'fantasy_name': 'IRONA',
                'legal_name': 'Baragiola-Zanitti SH',
                'slogan': 'tfw no slogan',
                'initiated_activities': '2016-01-01'
            },
            'fiscal_position': (
                reverse('api:invoice:fiscalposition-detail', args=[1])
            ),
            'fiscal_address': {
                'street_address': '9 de Julio 2454',
                'floor_number': '',
                'apartment_number': '',
                'locality': reverse('api:geo:locality-detail', args=[1]),
                'postal_code': '3000'
            },
            'default_invoice_debit_account': null,
            'default_invoice_credit_account': null
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.CompanyInvoice.objects.filter(
            persons_company__fantasy_name='IRONA'
        ).delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.CompanyInvoice.objects.count(), 1)

    def test_correctness(self):
        obj = models.CompanyInvoice.objects.get(
            persons_company__fantasy_name='IRONA'
        )
        self.assertEqual(
            obj.persons_company.fantasy_name,
            'IRONA'
        )
        self.assertEqual(
            obj.persons_company.legal_name,
            'Baragiola-Zanitti SH'
        )
        self.assertEqual(
            obj.persons_company.slogan,
            'tfw no slogan'
        )
        self.assertEqual(
            obj.persons_company.initiated_activities,
            date(2016, 1, 1)
        )
        self.assertEqual(
            obj.fiscal_position,
            models.FiscalPosition.objects.get(name='Do Easy')
        )
        self.assertEqual(
            obj.fiscal_address.street_address,
            '9 de Julio 2454'
        )
        self.assertEqual(
            obj.fiscal_address.floor_number,
            ''
        )
        self.assertEqual(
            obj.fiscal_address.apartment_number,
            ''
        )
        self.assertEqual(
            obj.fiscal_address.locality,
            Locality.objects.get(pk=1)
        )
        self.assertEqual(
            obj.fiscal_address.postal_code,
            '3000'
        )


class ContactInvoiceTestCase(APITestCase):
    """
    """
    fixtures = [
        'invoice/tests/fixtures/users.json',
        'invoice/tests/fixtures/geo.json',
        'invoice/tests/fixtures/companies.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:invoice:contactinvoice-list')
        data = {
            'persons_company': (
                reverse('api:persons:company-detail', args=[1])
            ),
            'name': 'Tobias Riper',
            'birth_date': '1970-07-07',
            'born_in': reverse('api:geo:country-detail', args=[1]),
            'phone_numbers': '555444555,333222333',
            'extra_emails': (
                'they.said.this.wouldnt.fit@gmail.com,topkek@hotmail.com'
            ),
            'contact_type': 'I',
            'home_address': {
                'street_address': '9 de Julio 2454',
                'floor_number': '',
                'apartment_number': '',
                'locality': reverse('api:geo:locality-detail', args=[1]),
                'postal_code': '3000'
            }
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.Contact.objects.filter(name='Tobias Riper').delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Contact.objects.count(), 1)

    def test_correctness(self):
        obj = models.Contact.objects.get(name='Tobias Riper')
        self.assertEqual(
            obj.persons_company,
            Company.objects.get(fantasy_name='IRONA')
        )
        self.assertEqual(
            obj.name,
            'Tobias Riper'
        )
        self.assertEqual(
            obj.birth_date,
            date(1970, 7, 7)
        )
        self.assertEqual(
            obj.born_in,
            Country.objects.get(pk=1)
        )
        self.assertEqual(
            obj.phone_numbers,
            '555444555,333222333'
        )
        self.assertEqual(
            obj.extra_emails,
            'they.said.this.wouldnt.fit@gmail.com,topkek@hotmail.com'
        )
        self.assertEqual(
            obj.contact_type,
            'I'
        )
        self.assertEqual(
            obj.home_address.street_address,
            '9 de Julio 2454'
        )
        self.assertEqual(
            obj.home_address.floor_number,
            ''
        )
        self.assertEqual(
            obj.home_address.apartment_number,
            ''
        )
        self.assertEqual(
            obj.home_address.locality,
            Locality.objects.get(pk=1)
        )
        self.assertEqual(
            obj.home_address.postal_code,
            '3000'
        )

    def test_birthdate(self):
        data = {
            'birth_date': str(date.today())
        }
        obj = models.Contact.objects.get(name='Tobias Riper')
        url = reverse('api:contact:contact-detail', args=[obj.pk])
        self.response = self.client.put(url, data)
        self.assertEqual(
            self.response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
