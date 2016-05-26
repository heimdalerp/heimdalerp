from cities_light.models import Country
from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        PrimaryKeyRelatedField)

from contact import models
from persons.models import PhysicalAddress
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

    def create(self, validated_data):
        home_address_data = validated_data.pop('home_address')
        home_address = PhysicalAddress.objects.create(**home_address_data)
        validated_data['home_address'] = home_address
        contact = models.Contact.objects.create(**validated_data)
        return contact

    def update(self, instance, validated_data):
        home_address_data = validated_data.pop('home_address')
        home_address = PhysicalAddress.objects.update_or_create(
            **home_address_data
        )
        validated_data['home_address'] = home_address
        instance.update(**validated_data)
        return instance
