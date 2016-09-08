from persons import models, serializers
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


class PhysicalAddressViewSet(ReadOnlyModelViewSet):
    queryset = models.PhysicalAddress.objects.all()
    serializer_class = serializers.PhysicalAddressSerializer


class CompanyViewSet(ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
