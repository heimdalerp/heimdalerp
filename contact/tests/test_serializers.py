from datetime import date

from contact import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from geo.models import Country, Locality
from persons.models import Company
from rest_framework import status
from rest_framework.test import APITestCase


class ContactTestCase(APITestCase):
    """
    """
    fixtures = [
        'contact/tests/fixtures/users.json',
        'contact/tests/fixtures/geo.json',
        'contact/tests/fixtures/companies.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:contact:contact-list')
        data = {
            'persons_company': (
                reverse(
                    'api:persons:company-detail',
                    args=[Company.objects.get(fantasy_name='IRONA').pk]
                )
            ),
            'name': 'Tobias Riper',
            'birth_date': '1970-07-07',
            'born_in': reverse(
                'api:geo:country-detail',
                args=[Country.objects.get(default_name='Argentina').pk]
            ),
            'phone_numbers': '555444555,333222333',
            'extra_emails': (
                'they.said.this.wouldnt.fit@gmail.com,topkek@hotmail.com'
            ),
            'contact_type': 'I',
            'home_address': {
                'street_address': '9 de Julio 2454',
                'floor_number': '',
                'apartment_number': '',
                'locality': reverse(
                    'api:geo:locality-detail',
                    args=[Locality.objects.get(default_name='Santa Fe').pk]
                ),
                'postal_code': '3000'
            }
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.Contact.objects.get().delete()

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
            Country.objects.get(default_name='Argentina')
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
            Locality.objects.get(default_name='Santa Fe')
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
