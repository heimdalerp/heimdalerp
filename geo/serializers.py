from rest_framework.serializers import (HyperlinkedIdentityField,
                                        HyperlinkedModelSerializer)

from geo import models


class AlternativeNameSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.AlternativeName
        fields = (
            'url',
            'id',
            'name',
            'language_code',
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:geo:alternativename-detail'
            }
        }


class LocalitySerializer(HyperlinkedModelSerializer):
    alternative_names = AlternativeNameSerializer(many=True)

    class Meta:
        model = models.Locality
        fields = (
            'url',
            'id',
            'default_name',
            'alternative_names',
            'region'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:geo:locality-detail'
            },
            'region': {
                'view_name': 'api:geo:region-detail'
            }
        }


class RegionSerializer(HyperlinkedModelSerializer):
    alternative_names = AlternativeNameSerializer(many=True)
    localities = HyperlinkedIdentityField(
        view_name='api:geo:region-localities'
    )

    class Meta:
        model = models.Region
        fields = (
            'url',
            'id',
            'default_name',
            'alternative_names',
            'codename',
            'country',
            'localities'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:geo:region-detail',
            },
            'country': {
                'view_name': 'api:geo:country-detail'
            }
        }


class CountrySerializer(HyperlinkedModelSerializer):
    alternative_names = AlternativeNameSerializer(many=True)
    regions = HyperlinkedIdentityField(
        view_name='api:geo:country-regions'
    )
    localities = HyperlinkedIdentityField(
        view_name='api:geo:country-localities'
    )

    class Meta:
        model = models.Country
        fields = (
            'url',
            'id',
            'default_name',
            'alternative_names',
            'codename',
            'regions',
            'localities'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:geo:country-detail'
            }
        }
