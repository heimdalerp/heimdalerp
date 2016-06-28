from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from geo import models, serializers


class AlternativeNameViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.AlternativeNameSerializer
    queryset = models.AlternativeName.objects.all()


class CountryViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.CountrySerializer
    queryset = models.Country.objects.all()


class RegionViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.RegionSerializer
    queryset = models.Region.objects.all()


class RegionsByCountryList(ListAPIView):
    serializer_class = serializers.RegionSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Region.objects.filter(country=pk)


class LocalityViewSet(ModelViewSet):
    serializer_class = serializers.LocalitySerializer
    queryset = models.Locality.objects.all()

    def get_queryset(self):
        """
        Allows a GET param, 'q', to be used against search_names.
        """
        queryset = super(ModelViewSet, self).get_queryset()

        if self.request.GET.get('q', None):
            return queryset.filter(
                search_names__icontains=self.request.GET['q'])

        return queryset


class LocalitiesByCountryList(ListAPIView):
    serializer_class = serializers.LocalitySerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Locality.objects.filter(region__country=pk)


class LocalitiesByRegionList(ListAPIView):
    serializer_class = serializers.LocalitySerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Locality.objects.filter(region=pk)
