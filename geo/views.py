from cities.models import District, City, Subregion, Region, Country
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from geo import serializers


class CountryViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.CountrySerializer
    queryset = Country.objects.all()
    lookup_field = 'code'
    lookup_value_regex = '[a-zA-Z]+'


class RegionViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.RegionSerializer
    queryset = Region.objects.all()
    lookup_field = 'code'
    lookup_value_regex = '[a-zA-Z]+'


class RegionsByCountryList(ListAPIView):
    serializer_class = serializers.RegionSerializer

    def get_queryset(self):
        code = self.kwargs['code']
        return Region.objects.filter(country__code=code)


class SubregionViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.SubregionSerializer
    queryset = Subregion.objects.all()
    lookup_field = 'code'
    lookup_value_regex = '[a-zA-Z]+'


class SubregionsByRegionList(ListAPIView):
    serializer_class = serializers.SubregionSerializer

    def get_queryset(self):
        code = self.kwargs['code']
        return Subregion.objects.filter(region__code=code)


class CityViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.CitySerializer
    queryset = City.objects.all()
    lookup_field = 'code'
    lookup_value_regex = '[a-zA-Z]+'

    def get_queryset(self):
        """
        Allows a GET param, 'q', to be used against search_names.
        """
        queryset = super(ReadOnlyModelViewSet, self).get_queryset()

        if self.request.GET.get('q', None):
            return queryset.filter(
                search_names__icontains=self.request.GET['q'])

        return queryset


class CitiesByCountryList(ListAPIView):
    serializer_class = serializers.CitySerializer

    def get_queryset(self):
        code = self.kwargs['code']
        return City.objects.filter(country__code=code)


class CitiesByRegionList(ListAPIView):
    serializer_class = serializers.CitySerializer

    def get_queryset(self):
        code = self.kwargs['code']
        return City.objects.filter(region__code=code)


class DistrictViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.DistrictSerializer
    queryset = District.objects.all()


class DistrictsByCityList(ListAPIView):
    serializer_class = serializers.DistrictSerializer

    def get_queryset(self):
        code = self.kwargs['code']
        return District.objects.filter(city__code=code)
