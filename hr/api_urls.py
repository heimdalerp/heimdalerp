from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from hr import views


router = DefaultRouter()
router.register(r'ethnicities', views.EthnicityViewSet)
router.register(r'sexualorientations', views.SexualOrientationViewSet)
router.register(r'aptitudes', views.AptitudeViewSet)
router.register(r'achievements', views.AchievementViewSet)
router.register(r'sanctions', views.SanctionViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'languages', views.LanguageViewSet)
router.register(
    r'employeesspeaklanguages',
    views.EmployeeSpeaksLanguageViewSet
)
router.register(
    r'employeeshavesanctions',
    views.EmployeeHasSanctionViewSet
)
router.register(r'academicinstitutions', views.AcademicInstitutionViewSet)
router.register(r'degrees', views.DegreeViewSet)
router.register(r'employeeshavedegrees', views.EmployeeHasDegreeViewSet)

app_name = 'hr'
urlpatterns = [
    url(r'^', include(router.urls)),
]

