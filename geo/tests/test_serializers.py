from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from geo import models


class LocalityTestCase(APITestCase):
    """
    """
    fixtures = [
        'persons/tests/fixtures/users.json',
        'persons/tests/fixtures/geo.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:geo:locality-list')
        data = {
            'default_name': 'Santa Fe',
            'alternative_names': [
                {
                    'name': 'Santa Fe',
                    'language_code': 'en'
                },
                {
                    'name': 'Santa Fe',
                    'language_code': 'es'
                }
            ],
            'region': reverse(
                'api:geo:region-detail',
                args=[models.Region.objects.get(default_name='Santa Fe').pk]
            )
        }  
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.Locality.objects.filter(
            name='Santa Fe'
        ).delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Locality.objects.count(), 1)

    def test_correctness(self):
        obj = models.Locality.objects.get(
            name='Santa Fe'
        )
        self.assertEqual(obj.name, 'Santa Fe')
        self.assertEqual(
            obj.region,
            models.Region.objects.get(default_name='Santa Fe')
        )
