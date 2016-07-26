from django.db import transaction
from geo import models
from rest_framework.serializers import (HyperlinkedIdentityField,
                                        HyperlinkedModelSerializer)


class AlternativeNameSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.AlternativeName
        fields = (
            'url',
            'id',
            'name',
            'language_code',
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:geo:alternativename-detail'
            }
        }


class LocalitySerializer(HyperlinkedModelSerializer):
    alternative_names = AlternativeNameSerializer(many=True)

    class Meta:
        model = models.Locality
        fields = (
            'url',
            'id',
            'default_name',
            'alternative_names',
            'region'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:geo:locality-detail'
            },
            'region': {
                'view_name': 'api:geo:region-detail'
            }
        }

    @transaction.atomic
    def create(self, validated_data):
        alternative_names_data = validated_data.pop('alternative_names')
        locality = models.Locality.objects.create(
            **validated_data
        )

        if alternative_names_data is not None:
            for a_n_data in alternative_names_data:
                alternative_name = models.AlternativeName.objects.create(
                    **a_n_data
                )
                locality.alternative_names.add(alternative_name)

        return locality

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.default_name = validated_data.get(
            'default_name',
            instance.default_name
        )
        instance.region = validated_data.get(
            'region',
            instance.region
        )

        alternative_names_data = validated_data.pop('alternative_names')
        if alternative_names_data is not None:
            instance.alternative_names.clear()
            for a_l_data in alternative_names_data:
                alternative_name = (
                        models.AlternativeName.objects.create(**a_l_data)
                    )
                instance.alternative_names.add(alternative_name)

        instance.save()
        return instance


class RegionSerializer(HyperlinkedModelSerializer):
    alternative_names = AlternativeNameSerializer(many=True)
    localities = HyperlinkedIdentityField(
        view_name='api:geo:region-localities'
    )

    class Meta:
        model = models.Region
        fields = (
            'url',
            'id',
            'default_name',
            'alternative_names',
            'codename',
            'country',
            'localities'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:geo:region-detail',
            },
            'country': {
                'view_name': 'api:geo:country-detail'
            }
        }


class CountrySerializer(HyperlinkedModelSerializer):
    alternative_names = AlternativeNameSerializer(many=True)
    regions = HyperlinkedIdentityField(
        view_name='api:geo:country-regions'
    )
    localities = HyperlinkedIdentityField(
        view_name='api:geo:country-localities'
    )

    class Meta:
        model = models.Country
        fields = (
            'url',
            'id',
            'default_name',
            'alternative_names',
            'codename',
            'regions',
            'localities'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:geo:country-detail'
            }
        }
