from cities_light.models import Country
from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        SlugRelatedField)

from contact import models
from persons.models import PhysicalAddress
from persons.serializers import PhysicalAddressSerializer


class ContactSerializer(HyperlinkedModelSerializer):
    born_in = SlugRelatedField(
        slug_field='geoname_id',
        queryset=Country.objects.all(),
        allow_null=True
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
            },
            'born_in': {
                'required': False
            },
            'home_address': {
                'required': False
            }
        }

    def create(self, validated_data):
        home_address_data = validated_data.get('home_address', None)
        if home_address_data is not None and (
            home_address_data['street_address'] is not ''
        ):
            home_address = PhysicalAddress.objects.create(
                **home_address_data
            )
            validated_data['home_address'] = home_address
        
        contact = models.Contact.objects.create(**validated_data)
        return contact

    def update(self, instance, validated_data):
        home_address_data = validated_data.get('home_address', None)
        if home_address_data is not None and (
            home_address_data['street_address'] is not ''
        ):
            home_address = PhysicalAddress.objects.update_or_create(
                **home_address_data
            )
            validated_data['home_address'] = home_address
        instance.update(**validated_data)
        return instance
