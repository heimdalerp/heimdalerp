from rest_framework.serializers import HyperlinkedModelSerializer

from persons import models


class PhoneNumberSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.PhoneNumber


class ExtraEmailAddressSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.ExtraEmailAddress


class PhysicalAddressSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.PhysicalAddress

