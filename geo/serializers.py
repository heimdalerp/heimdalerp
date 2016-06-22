from cities.models import (AlternativeName, City, District, Subregion,
                            Region, Country)
from rest_framework.serializers import (HyperlinkedIdentityField,
                                        HyperlinkedModelSerializer)


class AlternativeNameSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = AlternativeName
        fields = (
            'url',
            'id',
            'name',
            'language',
            'is_preferred',
            'is_short',
            'is_colloquial'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:geo:alternativename-detail'
            }
        }


class DistrictSerializer(HyperlinkedModelSerializer):
    alt_names = AlternativeNameSerializer(many=True)

    class Meta:
        model = District
        fields = (
            'url',
            'id',
            'name',
            'slug',
            'alt_names',
            'name_std',
            'city'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:geo:district-detail'
            },
            'city': {
                'view_name': 'api:geo:city-detail',
                'lookup_field': 'code'
            }
        }


class CitySerializer(HyperlinkedModelSerializer):
    alt_names = AlternativeNameSerializer(many=True)

    class Meta:
        model = City
        fields = (
            'url',
            'id',
            'name',
            'slug',
            'alt_names',
            'name_std',
            'subregion',
            'region',
            'country',
            'districts'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:geo:city-detail',
                'lookup_field': 'code'
            },
            'subregion': {
                'view_name': 'api:geo:subregion-detail',
                'lookup_field': 'code'
            },
            'region': {
                'view_name': 'api:geo:region-detail',
                'lookup_field': 'code'
            },
            'country': {
                'view_name': 'api:geo:country-detail',
                'lookup_field': 'code'
            }
        }


class SubregionSerializer(HyperlinkedModelSerializer):
    alt_names = AlternativeNameSerializer(many=True)

    class Meta:
        model = Subregion
        fields = (
            'url',
            'id',
            'name',
            'slug',
            'alt_names',
            'name_std',
            'code',
            'region'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:geo:subregion-detail',
                'lookup_field': 'code'
            },
            'region': {
                'view_name': 'api:geo:region-detail',
                'lookup_field': 'code'
            }
        }


class RegionSerializer(HyperlinkedModelSerializer):
    alt_names = AlternativeNameSerializer(many=True)
    subregions = HyperlinkedIdentityField(
        view_name='api:geo:region-subregions',
        lookup_field='code'
    )
    cities = HyperlinkedIdentityField(
        view_name='api:geo:region-cities',
        lookup_field='code'
    )

    class Meta:
        model = Region
        fields = (
            'url',
            'id',
            'name',
            'slug',
            'alt_names',
            'name_std',
            'code',
            'country',
            'subregions',
            'cities'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:geo:region-detail',
                'lookup_field': 'code'
            },
            'country': {
                'view_name': 'api:geo:country-detail',
                'lookup_field': 'code'
            }
        }


class CountrySerializer(HyperlinkedModelSerializer):
    alt_names = AlternativeNameSerializer(many=True)
    regions = HyperlinkedIdentityField(
        view_name='api:geo:country-regions',
        lookup_field='code'
    )
    cities = HyperlinkedIdentityField(
        view_name='api:geo:country-cities',
        lookup_field='code'
    )

    class Meta:
        model = Country
        fields = (
            'url',
            'id',
            'name',
            'slug',
            'alt_names',
            'code',
            'languages',
            'regions',
            'cities'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:geo:country-detail',
                'lookup_field': 'code'
            }
        }
