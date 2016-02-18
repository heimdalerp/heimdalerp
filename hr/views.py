from rest_framework.viewsets import ModelViewSet

from hr import models, serializers


class EthnicityViewSet(ModelViewSet):
    queryset = models.Ethnicity.objects.all()
    serializer_class = serializers.EthnicitySerializer


class SexualOrientationViewSet(ModelViewSet):
    queryset = models.Ethnicity.objects.all()
    serializer_class = serializers.SexualOrientationSerializer


class AptitudeViewSet(ModelViewSet):
    queryset = models.Aptitude.objects.all()
    serializer_class = serializers.AptitudeSerializer


class AchievementViewSet(ModelViewSet):
    queryset = models.Achievement.objects.all()
    serializer_class = serializers.AchievementSerializer


class SanctionViewSet(ModelViewSet):
    queryset = models.Sanction.objects.all()
    serializer_class = serializers.SanctionSerializer


class EmployeeViewSet(ModelViewSet):
    queryset = models.Ethnicity.objects.all()
    serializer_class = serializers.EthnicitySerializer


class LanguageViewSet(ModelViewSet):
    queryset = models.Language.objects.all()
    serializer_class = serializers.EthnicitySerializer


class EmployeeSpeaksLanguageViewSet(ModelViewSet):
    queryset = models.EmployeeSpeaksLanguage.objects.all()
    serializer_class = serializers.EmployeeSpeaksLanguageSerializer


class EmployeeHasSanctionViewSet(ModelViewSet):
    queryset = models.EmployeeHasSanction.objects.all()
    serializer_class = serializers.EmployeeHasSanctionSerializer


class AcademicInstitutionViewSet(ModelViewSet):
    queryset = models.AcademicInstitution.objects.all()
    serializer_class = serializers.AcademicInstitutionSerializer


class DegreeViewSet(ModelViewSet):
    queryset = models.Degree.objects.all()
    serializer_class = serializers.DegreeSerializer


class EmployeeHasDegreeViewSet(ModelViewSet):
    queryset = models.EmployeeHasDegree.objects.all()
    serializer_class = serializers.EmployeeHasDegreeSerializer

