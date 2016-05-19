from rest_framework.serializers import HyperlinkedModelSerializer

from contact import models


class ContactSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Contact
        fields = (
            'url',
            'id',
            'name',
            'contact_type'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:contact:contact-detail'
            }
        }


