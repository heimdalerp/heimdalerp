from rest_framework.viewsets import ModelViewSet

from persons import models, serializers


class PhysicalAddressViewSet(ModelViewSet):
    queryset = models.PhysicalAddress.objects.all()
    serializer_class = serializers.PhysicalAddressSerializer


class CompanyViewSet(ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
