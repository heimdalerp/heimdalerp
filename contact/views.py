from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from contact import models, serializers


class ContactViewSet(ModelViewSet):
    queryset = models.Contact.objects.all()
    serializer_class = serializers.ContactSerializer


class ContactsByCompanyList(ListAPIView):
    serializer_class = serializers.ContactSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Contact.objects.filter(persons_company=pk)
