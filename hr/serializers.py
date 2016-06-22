from cities.models import Country
from django.contrib.auth.models import User
from rest_framework.serializers import (HyperlinkedIdentityField,
                                        HyperlinkedModelSerializer,
                                        ModelSerializer,
                                        SlugRelatedField)

from hr import models
from persons.serializers import PhysicalAddressSerializer


class UserSerializer(ModelSerializer):

    class Meta:
            model = User
            fields = (
                'id',
                'first_name',
                'last_name',
                'email',
                'is_active',
                'groups'
            )


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
    user = UserSerializer()
    born_in = SlugRelatedField(
        slug_field='geoname_id',
        queryset=Country.objects.all(),
        required=False
    )
    home_address = PhysicalAddressSerializer()
    ethnicities = EthnicitySerializer(many=True)
    sexual_orientation = SexualOrientationSerializer()

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
    areas = HyperlinkedIdentityField(
        view_name='api:hr:employee-areas'
    )
    roles = HyperlinkedIdentityField(
        view_name='api:hr:employee-roles'
    )

    class Meta:
        model = models.Employee
        fields = (
            'url',
            'id',
            'persons_company',
            'user',
            'birth_date',
            'born_in',
            'phone_numbers',
            'extra_emails',
            'home_address',
            'genre',
            'ethnicities',
            'sexual_orientation',
            'aptitudes',
            'achievements',
            'languages',
            'sanctions',
            'degrees',
            'areas',
            'roles'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:hr:employee-detail'
            },
            'persons_company': {
                'view_name': 'api:persons:company-detail'
            },
            'sexual_orientation': {
                'required': False
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


class RoleSerializer(HyperlinkedModelSerializer):
    employees = HyperlinkedIdentityField(
        view_name='api:hr:role-employees'
    )

    class Meta:
        model = models.Role
        fields = (
            'url',
            'id',
            'name',
            'points',
            'employees'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:hr:role-detail'
            }
        }


class AreaSerializer(HyperlinkedModelSerializer):
    employees = HyperlinkedIdentityField(
        view_name='api:hr:area-employees'
    )

    class Meta:
        model = models.Area
        fields = (
            'url',
            'id',
            'persons_company',
            'name',
            'points',
            'employees'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:hr:area-detail'
            },
            'persons_company': {
                'view_name': 'api:persons:company-detail'
            }
        }


class AreaHasEmployeeSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.AreaHasEmployee
        fields = (
            'url',
            'id',
            'area',
            'employee',
            'date_since'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:hr:areahasemployee-detail'
            },
            'area': {
                'view_name': 'api:hr:area-detail'
            },
            'employee': {
                'view_name': 'api:hr:employee-detail'
            }
        }


class EmployeeHasRoleSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.EmployeeHasRole
        fields = (
            'url',
            'id',
            'role',
            'employee',
            'date_since'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:hr:employeehasrole-detail'
            },
            'role': {
                'view_name': 'api:hr:role-detail'
            },
            'employee': {
                'view_name': 'api:hr:employee-detail'
            }
        }
