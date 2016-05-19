from rest_framework.viewsets import ModelViewSet

from contact import models, serializers


class ContactViewSet(ModelViewSet):
    queryset = models.Contact.objects.all()
    serializer_class = serializers.ContactSerializer
