from rest_framework.serializers import HyperlinkedModelSerializer

from hr import models


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

    class Meta:
        model = models.Employee


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

