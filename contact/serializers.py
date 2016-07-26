from contact import models
from persons.models import PhysicalAddress
from persons.serializers import PhysicalAddressSerializer
from rest_framework.serializers import HyperlinkedModelSerializer


class ContactSerializer(HyperlinkedModelSerializer):
    home_address = PhysicalAddressSerializer()

    class Meta:
        model = models.Contact
        fields = (
            'url',
            'id',
            'persons_company',
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
            'persons_company': {
                'view_name': 'api:persons:company-detail'
            },
            'born_in': {
                'view_name': 'api:geo:country-detail',
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
        instance.home_address.street_address = home_address_data.get(
            'street_address', instance.home_address.street_address
        )
        instance.home_address.floor_number = home_address_data.get(
            'floor_number', instance.home_address.floor_number
        )
        instance.home_address.apartment_number = home_address_data.get(
            'apartment_number', instance.home_address.apartment_number
        )
        instance.home_address.city = home_address_data.get(
            'city', instance.home_address.city
        )
        instance.home_address.postal_code = home_address_data.get(
            'postal_code', instance.home_address.postal_code
        )
        instance.home_address.save()

        instance.persons_company = validated_data.get(
            'persons_company', instance.persons_company
        )
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
