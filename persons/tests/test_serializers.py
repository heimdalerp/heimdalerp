from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from persons import models


class PhysicalAddressTestCase(APITestCase):
    """
    """
    def test_create(self):
        url = reverse('api:persons:physicaladdress-list')  
