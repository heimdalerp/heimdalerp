from cities.models import (AlternativeName, District, City, Subregion,
                            Region, Country)
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from geo import serializers


class AlternativeNameViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.AlternativeNameSerializer
    queryset = AlternativeName.objects.all()


class CountryViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.CountrySerializer
    queryset = Country.objects.all()


class RegionViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.RegionSerializer
    queryset = Region.objects.all()


class RegionsByCountryList(ListAPIView):
    serializer_class = serializers.RegionSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Region.objects.filter(country=pk)


class SubregionViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.SubregionSerializer
    queryset = Subregion.objects.all()

class SubregionsByRegionList(ListAPIView):
    serializer_class = serializers.SubregionSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Subregion.objects.filter(region=pk)


class CityViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.CitySerializer
    queryset = City.objects.all()

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
        pk = self.kwargs['pk']
        return City.objects.filter(country=pk)


class CitiesByRegionList(ListAPIView):
    serializer_class = serializers.CitySerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return City.objects.filter(region=pk)


class DistrictViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.DistrictSerializer
    queryset = District.objects.all()


class DistrictsByCityList(ListAPIView):
    serializer_class = serializers.DistrictSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return District.objects.filter(city=pk)
