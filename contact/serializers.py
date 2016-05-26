from cities_light.models import Country
from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        PrimaryKeyRelatedField)

from contact import models
from persons.serializers import (ExtraEmailAddressSerializer,
                                 PhoneNumberSerializer)


class ContactSerializer(HyperlinkedModelSerializer):
    phone_numbers = PhoneNumberSerializer(many=True)
    extra_emails = ExtraEmailAddressSerializer(many=True)
    born_in = PrimaryKeyRelatedField(
        queryset=Country.objects.all()
    )

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
            'contact_type'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:contact:contact-detail'
            }
        }
