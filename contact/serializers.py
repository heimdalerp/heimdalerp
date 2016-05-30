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
        home_address_data = validated_data.pop('home_address')
        home_address = PhysicalAddress.objects.create(
            **home_address_data
        )
        validated_data['home_address'] = home_address

        contact = models.Contact.objects.create(**validated_data)
        return contact

    def update(self, instance, validated_data):
        home_address_data = validated_data.pop('home_address')
        home_address = PhysicalAddress.objects.update_or_create(
            **home_address_data
        )
        validated_data['home_address'] = home_address

        instance.birth_date = validated_data.get(
            'birth_date', instance.birth_date
        )
        instance.born_in = validated_data.get('born_in', instance.born_in)
        instance.phone_numbers = validated_data.get(
            'phone_numbers', instance.phone_numbers
        )
        instance.extra_emails = validated_data.get(
            'extra_emails', instance.extra_emails
        )
        instance.name = validated_data.get('name', instance.name)
        instance.contact_type = validated_data.get(
            'contact_type', instance.contact_type
        )

        instance.save()
        return instance
