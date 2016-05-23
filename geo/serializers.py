from cities_light.loading import get_cities_models
from rest_framework.serializers import (HyperlinkedIdentityField,
                                        HyperlinkedModelSerializer,
                                        HyperlinkedRelatedField)

Country, Region, City = get_cities_models()


class CitySerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='api:geo:city-detail'
    )
    country = HyperlinkedRelatedField(
        view_name='api:geo:country-detail',
        read_only=True
    )
    region = HyperlinkedRelatedField(
        view_name='api:geo:region-detail',
        read_only=True
    )

    class Meta:
        model = City
        exclude = ('slug',)


class RegionSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='api:geo:region-detail'
    )
    country = HyperlinkedRelatedField(
        view_name='api:geo:country-detail',
        read_only=True
    )
    cities = HyperlinkedIdentityField(
        view_name='api:geo:region-cities'
    )

    class Meta:
        model = Region
        exclude = ('slug',)


class CountrySerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='api:geo:country-detail'
    )
    regions = HyperlinkedIdentityField(
        view_name='api:geo:country-regions'
    )
    cities = HyperlinkedIdentityField(
        view_name='api:geo:country-cities'
    )

    class Meta:
        model = Country
