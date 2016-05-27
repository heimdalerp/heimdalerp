from cities_light.models import City
from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        PrimaryKeyRelatedField)

from persons import models


class PhysicalAddressSerializer(HyperlinkedModelSerializer):
    city = PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        required=False
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
