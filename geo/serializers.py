from cities_light.loading import get_cities_models
from rest_framework.serializers import (HyperlinkedIdentityField,
                                        HyperlinkedModelSerializer,
                                        HyperlinkedRelatedField)

Country, Region, City = get_cities_models()


class CitySerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='api:geo:city-detail',
        lookup_field='geoname_id'
    )
    country = HyperlinkedRelatedField(
        view_name='api:geo:country-detail',
        lookup_field='geoname_id',
        read_only=True
    )
    region = HyperlinkedRelatedField(
        view_name='api:geo:region-detail',
        lookup_field='geoname_id',
        read_only=True
    )

    class Meta:
        model = City
        fields = (
            'url',
            'id',
            'geoname_id',
            'name_ascii',
            'region',
            'country'
        )

class RegionSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='api:geo:region-detail',
        lookup_field='geoname_id'
    )
    country = HyperlinkedRelatedField(
        view_name='api:geo:country-detail',
        lookup_field='geoname_id',
        read_only=True
    )
    cities = HyperlinkedIdentityField(
        view_name='api:geo:region-cities',
        lookup_field='geoname_id'
    )

    class Meta:
        model = Region
        fields = (
            'url',
            'id',
            'geoname_id',
            'name_ascii',
            'country',
            'cities'
        )


class CountrySerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='api:geo:country-detail',
        lookup_field='geoname_id'
    )
    regions = HyperlinkedIdentityField(
        view_name='api:geo:country-regions',
        lookup_field='geoname_id'
    )
    cities = HyperlinkedIdentityField(
        view_name='api:geo:country-cities',
        lookup_field='geoname_id'
    )

    class Meta:
        model = Country
        fields = (
            'url',
            'id',
            'geoname_id',
            'name_ascii',
            'regions',
            'cities'
        )
