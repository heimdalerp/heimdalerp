from django.conf import settings

from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.serializers import HyperlinkedIdentityField
from cities_light.contrib.restframework3 import CountrySerializer

from hr import models


class UserSerializer(ModelSerializer):

    class Meta:
        model = settings.AUTH_USER_MODEL


class EthnicitySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Ethnicity


class SexualOrientationSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.SexualOrientation


class AptitudeSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Aptitude


class AchievementSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Achievement


class SanctionSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Sanction


class EmployeeSerializer(HyperlinkedModelSerializer):
    user = UserSerializer()
    born_in = CountrySerializer()
    ## TODO: Decide if it is better to nest the relation or hyperlink it.
    #phone_numbers = persons_serializers.PhoneNumberSerializer()
    #extra_emails = persons_serializers.ExtraEmailSerializer()    

    ethnicities = HyperlinkedIdentityField(
        view_name='api:hr:employee-ethnicities'
    )
    aptitudes = HyperlinkedIdentityField(
        view_name='api:hr:employee-aptitudes'
    )
    achievements = HyperlinkedIdentityField(
        view_name='api:hr:employee-achievements'
    )
    sanctions = HyperlinkedIdentityField(
        view_name='api:hr:employee-sanctions'
    )
    languages = HyperlinkedIdentityField(
        view_name='api:hr:employee-languages'
    )
    degrees = HyperlinkedIdentityField(
        view_name='api:hr:employee-degrees'
    )

    class Meta:
        model = models.Employee
        fields = (
            'url',
            'id',
            'user',
            'birth_date',
            'born_in',
            'phone_numbers',
            'extra_emails',
            'genre',
            'member_since',
            'ethnicities',
            'sexual_orientation',
            'aptitudes',
            'achievements',
            'languages',
            'sanctions',
            'degrees'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:hr:employee-detail'
            },
            'phone_numbers': {
                'view_name': 'api:persons:phonenumber-list'
            },
            'extra_emails': {
                'view_name': 'api:persons:extraemail-list'
            }
        }


class LanguageSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Language


class EmployeeSpeaksLanguageSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.EmployeeSpeaksLanguage


class EmployeeHasSanctionSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.EmployeeHasSanction


class AcademicInstitutionSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.AcademicInstitution


class DegreeSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Degree


class EmployeeHasDegreeSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.EmployeeHasDegree

