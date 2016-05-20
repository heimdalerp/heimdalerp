from rest_framework.viewsets import ReadOnlyModelViewSet

from cities_light.models import City, Region, Country

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


class RegionModelViewSet(CitiesLightListModelViewSet):
    serializer_class = serializers.RegionSerializer
    queryset = Region.objects.all()


class CityModelViewSet(CitiesLightListModelViewSet):
    """
    ListRetrieveView for City.
    """
    serializer_class = serializers.CitySerializer
    queryset = City.objects.all()

    def get_queryset(self):
        """
        Allows a GET param, 'q', to be used against search_names.
        """
        queryset = super(CitiesLightListModelViewSet, self).get_queryset()

        if self.request.GET.get('q', None):
            return queryset.filter(
                search_names__icontains=self.request.GET['q'])

        return queryset
