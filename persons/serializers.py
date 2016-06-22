from cities.models import City
from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        SlugRelatedField)

from persons import models


class PhysicalAddressSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.PhysicalAddress
        fields = (
            'url',
            'id',
            'street_address',
            'floor_number',
            'apartment_number',
            'city',
            'postal_code'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:persons:physicaladdress-detail'
            },
            'city': {
                'view_name': 'api:geo:city-detail',
                'lookup_field': 'code',
                'required': False,
                'allow_null': True
            }
        }


class CompanySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Company
        fields = (
            'url',
            'id',
            'fantasy_name',
            'legal_name',
            'slogan',
            'initiated_activities',
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:persons:company-detail'
            }
        }
