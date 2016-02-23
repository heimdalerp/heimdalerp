from rest_framework.serializers import HyperlinkedModelSerializer
from cities_light.contrib.restframework3 import CitySerializer

from persons import models


class PhoneNumberSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.PhoneNumber
        fields = (
            'url',
            'id',
            'number',
            'phonenumber_type',
            'technology_type'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:persons:phonenumber-detail'
            }
        }


class ExtraEmailAddressSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.ExtraEmailAddress
        fields = (
            'url',
            'id',
            'email'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:persons:extraemailaddress-detail'
            }
        }


class PhysicalAddressSerializer(HyperlinkedModelSerializer):
    city = CitySerializer()

    class Meta:
        model = models.PhysicalAddress
        fields = (
            'url',
            'id',
            'address_type',
            'street_name',
            'street_number',
            'floor_number',
            'apartment_number',
            'city',
            'postal_code'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:persons:physicaladdress-detail'
            }
        }


class CompanySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Company
        fields = (
            'url',
            'id',
            'name',
            'initiated_activities'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:persons:company-detail'
            }
        }

