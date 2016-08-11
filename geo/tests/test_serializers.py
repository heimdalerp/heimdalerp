from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from geo import models
from rest_framework import status
from rest_framework.test import APITestCase


class CountryTestCase(APITestCase):
    """
    """
    fixtures = [
        'geo/tests/fixtures/users.json',
        'geo/tests/fixtures/geo.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:geo:country-list')
        data = {
            'default_name': 'Argentina'
        }
        self.response = self.client.post(url, data)

    def test_create(self):
        self.assertEqual(
            self.response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_update(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse(
            'api:geo:country-detail',
            args=[models.Country.objects.get(default_name='Argentina').pk]
        )
        data = {
            'default_name': 'Not Argentina',
        }
        response = self.client.put(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

class RegionTestCase(APITestCase):
    """
    """
    fixtures = [
        'geo/tests/fixtures/users.json',
        'geo/tests/fixtures/geo.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:geo:region-list')
        data = {
            'default_name': 'Santa Fe',
            'country': reverse(
                'api:geo:country-detail',
                args=[
                    models.Country.objects.get(default_name='Argentina').pk
                ]
            )
        }
        self.response = self.client.post(url, data)

    def test_create(self):
        self.assertEqual(
            self.response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_update(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse(
            'api:geo:region-detail',
            args=[models.Region.objects.get(default_name='Santa Fe').pk]
        )
        data = {
            'default_name': 'Holy Faith',
        }
        response = self.client.put(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )


class LocalityTestCase(APITestCase):
    """
    """
    fixtures = [
        'geo/tests/fixtures/users.json',
        'geo/tests/fixtures/geo.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:geo:locality-list')
        data = {
            'default_name': 'santa fe',
            'alternative_names': [
                {
                    'name': 'Holy Faith',
                    'language_code': 'en'
                },
                {
                    'name': 'Santa Fe',
                    'language_code': 'es'
                }
            ],
            'region': reverse(
                'api:geo:region-detail',
                args=[
                    models.Region.objects.get(default_name='Entre Ríos').pk
                ]
            )
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.Locality.objects.filter(default_name='Santa Fe').delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Locality.objects.count(), 1)

    def test_correctness(self):
        obj = models.Locality.objects.get(
            default_name='santa fe'
        )
        self.assertEqual(obj.default_name, 'santa fe')
        self.assertEqual(
            obj.alternative_names.all()[0].name,
            'Holy Faith'
        )
        self.assertEqual(
            obj.alternative_names.all()[0].language_code,
            'en'
        )
        self.assertEqual(
            obj.alternative_names.all()[1].name,
            'Santa Fe'
        )
        self.assertEqual(
            obj.alternative_names.all()[1].language_code,
            'es'
        )
        self.assertEqual(
            obj.region,
            models.Region.objects.get(default_name='Entre Ríos')
        )

    def test_update(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse(
            'api:geo:locality-detail',
            args=[models.Locality.objects.get(default_name='santa fe').pk]
        )
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
                },
                {
                    'name': 'Santa Fe',
                    'language_code': 'fr'
                }
            ],
            'region': reverse(
                'api:geo:region-detail',
                args=[models.Region.objects.get(default_name='Santa Fe').pk]
            )
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = models.Locality.objects.get(
            default_name='Santa Fe'
        )
        self.assertEqual(obj.default_name, 'Santa Fe')
        self.assertEqual(
            obj.alternative_names.all()[0].name,
            'Santa Fe'
        )
        self.assertEqual(
            obj.alternative_names.all()[0].language_code,
            'en'
        )
        self.assertEqual(
            obj.alternative_names.all()[1].name,
            'Santa Fe'
        )
        self.assertEqual(
            obj.alternative_names.all()[1].language_code,
            'es'
        )
        self.assertEqual(
            obj.alternative_names.all()[2].name,
            'Santa Fe'
        )
        self.assertEqual(
            obj.alternative_names.all()[2].language_code,
            'fr'
        )
        self.assertEqual(
            obj.region,
            models.Region.objects.get(default_name='Santa Fe')
        )
