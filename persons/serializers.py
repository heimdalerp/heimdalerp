from cities_light.models import City
from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        SlugRelatedField)

from persons import models


class PhysicalAddressSerializer(HyperlinkedModelSerializer):
    city = SlugRelatedField(
        slug_field='geoname_id',
        queryset=City.objects.all(),
        allow_null=True
    )

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
                'required': False
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
