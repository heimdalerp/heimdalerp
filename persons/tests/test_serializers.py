from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from persons import models


class PhysicalAddressTestCase(APITestCase):
    """
    """
    fixtures = [
        'persons/tests/fixtures/users.json',
        'persons/tests/fixtures/geo.json'
    ]

    def test_create(self):
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
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.PhysicalAddress.objects.count(), 1)
