from cities_light.models import Country
from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        PrimaryKeyRelatedField)

from contact import models
from persons.serializers import PhysicalAddressSerializer


class ContactSerializer(HyperlinkedModelSerializer):
    born_in = PrimaryKeyRelatedField(
        queryset=Country.objects.all()
    )
    home_address = PhysicalAddressSerializer()

    class Meta:
        model = models.Contact
        fields = (
            'url',
            'id',
            'name',
            'birth_date',
            'born_in',
            'phone_numbers',
            'extra_emails',
            'contact_type',
            'home_address'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:contact:contact-detail'
            }
        }
