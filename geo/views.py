from cities_light.models import City, Country, Region
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from geo import serializers


class CitiesLightListModelViewSet(ReadOnlyModelViewSet):
    def get_queryset(self):
        """
        Allows a GET param, 'q', to be used against name_ascii.
        """
        queryset = super(CitiesLightListModelViewSet, self).get_queryset()

        if self.request.GET.get('q', None):
            return queryset.filter(
                name_ascii__icontains=self.request.GET['q']
            )

        return queryset


class CountryModelViewSet(CitiesLightListModelViewSet):
    serializer_class = serializers.CountrySerializer
    queryset = Country.objects.all()
    lookup_field = 'geoname_id'
    lookup_value_regex = '[0-9]+'


class RegionModelViewSet(CitiesLightListModelViewSet):
    serializer_class = serializers.RegionSerializer
    queryset = Region.objects.all()
    lookup_field = 'geoname_id'
    lookup_value_regex = '[0-9]+'


class RegionsByCountryList(ListAPIView):
    serializer_class = serializers.RegionSerializer

    def get_queryset(self):
        geoname_id = self.kwargs['geoname_id']
        return Region.objects.filter(country__geoname_id=geoname_id)


class CityModelViewSet(CitiesLightListModelViewSet):
    """
    ListRetrieveView for City.
    """
    serializer_class = serializers.CitySerializer
    queryset = City.objects.all()
    lookup_field = 'geoname_id'
    lookup_value_regex = '[0-9]+'

    def get_queryset(self):
        """
        Allows a GET param, 'q', to be used against search_names.
        """
        queryset = super(CitiesLightListModelViewSet, self).get_queryset()

        if self.request.GET.get('q', None):
            return queryset.filter(
                search_names__icontains=self.request.GET['q'])

        return queryset


class CitiesByCountryList(ListAPIView):
    serializer_class = serializers.CitySerializer

    def get_queryset(self):
        geoname_id = self.kwargs['geoname_id']
        return City.objects.filter(country__geoname_id=geoname_id)


class CitiesByRegionList(ListAPIView):
    serializer_class = serializers.CitySerializer

    def get_queryset(self):
        geoname_id = self.kwargs['geoname_id']
        return City.objects.filter(region__geoname_id=geoname_id)
