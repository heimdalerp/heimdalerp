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
router.register(r'roles', views.RoleViewSet)
router.register(r'areas', views.AreaViewSet)
router.register(r'companyhaveemployees', views.CompanyHasEmployeeViewSet)
router.register(r'areahaveemployees', views.AreaHasEmployeeViewSet)
router.register(r'employeehaveroles', views.EmployeeHasRoleViewSet)

app_name = 'hr'
urlpatterns = [
    url(
        r'^employees/(?P<pk>\d+)/aptitudes/$',
        views.AptitudesByEmployeeList.as_view(),
        name='employee-aptitudes'
    ),
    url(
        r'^employees/(?P<pk>\d+)/achievements/$',
        views.AchievementsByEmployeeList.as_view(),
        name='employee-achievements'
    ),
    url(
        r'^employees/(?P<pk>\d+)/languages/$',
        views.LanguagesByEmployeeList.as_view(),
        name='employee-languages'
    ),
    url(
        r'^employees/(?P<pk>\d+)/sanctions/$',
        views.SanctionsByEmployeeList.as_view(),
        name='employee-sanctions'
    ),
    url(
        r'^employees/(?P<pk>\d+)/degrees/$',
        views.DegreesByEmployeeList.as_view(),
        name='employee-degrees'
    ),
    url(r'^', include(router.urls)),
]

