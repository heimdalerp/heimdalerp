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
        fields = (
            'url',
            'id',
            'name',
            'points'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:hr:ethnicity-detail'
            }
        }


class SexualOrientationSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.SexualOrientation
        fields = (
            'url',
            'id',
            'name',
            'points'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:hr:sexualorientation-detail'
            }
        }


class AptitudeSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Aptitude
        fields = (
            'url',
            'id',
            'name',
            'description',
            'points'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:hr:aptitude-detail'
            }
        }


class AchievementSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Achievement
        fields = (
            'url',
            'id',
            'description',
            'when_it_happened',
            'points'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:hr:achievement-detail'
            }
        }


class SanctionSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Sanction
        fields = (
            'url',
            'id',
            'name',
            'description',
            'points'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:hr:sanction-detail'
            }
        }


class EmployeeSerializer(HyperlinkedModelSerializer):
    #user = UserSerializer()
    #born_in = CountrySerializer()
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
            #'user',
            'birth_date',
            #'born_in',
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
        fields = (
            'url',
            'id',
            'name',
            'points',
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:hr:language-detail'
            }
        }


class EmployeeSpeaksLanguageSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.EmployeeSpeaksLanguage
        fields = (
            'url',
            'id',
            'employee',
            'language',
            'level',
            'points'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:hr:employeespeakslanguage-detail'
            },
            'employee': {
                'view_name': 'api:hr:employee-detail'
            },
            'language': {
                'view_name': 'api:hr:language-detail'
            }
        }


class EmployeeHasSanctionSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.EmployeeHasSanction
        fields = (
            'url',
            'id',
            'employee',
            'sanction',
            'what_happened',
            'when_it_happened',
            'others_implicated',
            'victims'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:hr:employeehassanction-detail'
            },
            'employee': {
                'view_name': 'api:hr:employee-detail'
            },
            'sanction': {
                'view_name': 'api:hr:sanction-detail'
            },
            'others_implicated': {
                'view_name': 'api:hr:employee-detail'
            },
            'victims': {
                'view_name': 'api:hr:employee-detail'
            }
        }


class AcademicInstitutionSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.AcademicInstitution
        fields = (
            'url',
            'id',
            'name',
            'points'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:hr:academicinstitution-detail'
            }
        }


class DegreeSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Degree
        fields = (
            'url',
            'id',
            'name',
            'points'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:hr:degree-detail'
            }
        }


class EmployeeHasDegreeSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.EmployeeHasDegree
        fields = (
            'url',
            'id',
            'employee',
            'degree',
            'academic_institution',
            'ingress_year',
            'egress_year'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:hr:employeehasdegree-detail'
            },
            'employee': {
                'view_name': 'api:hr:employee-detail'
            },
            'degree': {
                'view_name': 'api:hr:degree-detail'
            },
            'academic_institution': {
                'view_name': 'api:hr:academicinstitution-detail'
            }
        }

