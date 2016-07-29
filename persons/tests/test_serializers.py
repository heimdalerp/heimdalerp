from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from geo.models import Locality
from persons import models
from rest_framework import status
from rest_framework.test import APITestCase


class PhysicalAddressTestCase(APITestCase):
    """
    """
    fixtures = [
        'persons/tests/fixtures/users.json',
        'persons/tests/fixtures/geo.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:persons:physicaladdress-list')
        data = {
            'street_address': '9 de Julio 2454',
            'floor_number': '',
            'apartment_number': '',
            'locality': reverse(
                'api:geo:locality-detail',
                args=[
                    Locality.objects.get(default_name='Santa Fe').pk
                ]
            ),
            'postal_code': '3000'
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.PhysicalAddress.objects.filter(
            street_address='9 de Julio 2454'
        ).delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.PhysicalAddress.objects.count(), 1)

    def test_correctness(self):
        obj = models.PhysicalAddress.objects.get(
            street_address='9 de Julio 2454'
        )
        self.assertEqual(obj.street_address, '9 de Julio 2454')
        self.assertEqual(obj.floor_number, '')
        self.assertEqual(obj.apartment_number, '')
        self.assertEqual(
            obj.locality,
            Locality.objects.get(default_name='Santa Fe')
        )
        self.assertEqual(obj.postal_code, '3000')


class CompanyTestCase(APITestCase):
    """
    """
    fixtures = [
        'persons/tests/fixtures/users.json',
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:persons:company-list')
        data = {
            'fantasy_name': 'IRONA',
            'slogan': 'tfw no slogan'
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.Company.objects.filter(fantasy_name='IRONA').delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Company.objects.count(), 1)

    def test_correctness(self):
        obj = models.Company.objects.get()
        self.assertEqual(obj.fantasy_name, 'IRONA')
        self.assertEqual(obj.slogan, 'tfw no slogan')
