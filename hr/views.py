from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

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
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer


class EthnicitiesByEmployeeList(ListAPIView):
    serializer_class = serializers.EthnicitySerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        employee = models.Employee.objects.filter(pk=pk)
        return employee.ethnicities.all()


class AptitudesByEmployeeList(ListAPIView):
    serializer_class = serializers.AptitudeSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        employee = models.Employee.objects.filter(pk=pk)
        return employee.aptitudes.all()


class AchievementsByEmployeeList(ListAPIView):
    serializer_class = serializers.AchievementSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        employee = models.Employee.objects.filter(pk=pk)
        return employee.achievements.all()


class SanctionsByEmployeeList(ListAPIView):
    serializer_class = serializers.EmployeeHasSanctionSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.EmployeeHasSanction.objects.filter(employee=pk)


class LanguagesByEmployeeList(ListAPIView):
    serializer_class = serializers.EmployeeSpeaksLanguageSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.EmployeeSpeaksLanguage.objects.filter(employee=pk)


class DegreesByEmployeeList(ListAPIView):
    serializer_class = serializers.EmployeeHasDegreeSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.EmployeeHasDegree.objects.filter(employee=pk)


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

