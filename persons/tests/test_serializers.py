from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from geo.models import Locality
from persons import models


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
            'locality': reverse('api:geo:locality-detail', args=[1]),
            'postal_code': '3000'
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.PhysicalAddress.objects.filter(pk=1).delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.PhysicalAddress.objects.count(), 1)
        obj = models.PhysicalAddress.objects.get(pk=1)
        self.assertEqual(obj.street_address, '9 de Julio 2454')
        self.assertEqual(obj.locality, Locality.objects.get(pk=1))


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
            'legal_name': 'Baragiola-Zanitti SH',
            'slogan': '',
            'initiated_activities': '2016-01-01'
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.Company.objects.filter(pk=1).delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Company.objects.count(), 1)
