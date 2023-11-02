from django.urls import include, path
from hr import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('ethnicities', views.EthnicityViewSet)
router.register('sexualorientations', views.SexualOrientationViewSet)
router.register('aptitudes', views.AptitudeViewSet)
router.register('achievements', views.AchievementViewSet)
router.register('sanctions', views.SanctionViewSet)
router.register('employees', views.EmployeeViewSet)
router.register('languages', views.LanguageViewSet)
router.register(
    'employeesspeaklanguages',
    views.EmployeeSpeaksLanguageViewSet
)
router.register(
    'employeeshavesanctions',
    views.EmployeeHasSanctionViewSet
)
router.register('academicinstitutions', views.AcademicInstitutionViewSet)
router.register('degrees', views.DegreeViewSet)
router.register('employeeshavedegrees', views.EmployeeHasDegreeViewSet)
router.register('roles', views.RoleViewSet)
router.register('areas', views.AreaViewSet)
router.register('areahaveemployees', views.AreaHasEmployeeViewSet)
router.register('employeehaveroles', views.EmployeeHasRoleViewSet)

app_name = 'hr'
urlpatterns = [
    path(
        'employees/<pk>/aptitudes/',
        views.AptitudesByEmployeeList.as_view(),
        name='employee-aptitudes'
    ),
    path(
        'employees/<pk>/achievements/',
        views.AchievementsByEmployeeList.as_view(),
        name='employee-achievements'
    ),
    path(
        'employees/<pk>/languages/',
        views.LanguagesByEmployeeList.as_view(),
        name='employee-languages'
    ),
    path(
        'employees/<pk>/sanctions/',
        views.SanctionsByEmployeeList.as_view(),
        name='employee-sanctions'
    ),
    path(
        'employees/<pk>/degrees/',
        views.DegreesByEmployeeList.as_view(),
        name='employee-degrees'
    ),
    path(
        'employees/<pk>/areas/',
        views.AreasByEmployeeList.as_view(),
        name='employee-areas'
    ),
    path(
        'employees/<pk>/roles/',
        views.RolesByEmployeeList.as_view(),
        name='employee-roles'
    ),
    path(
        'roles/<pk>/employees/',
        views.EmployeesByRoleList.as_view(),
        name='role-employees'
    ),
    path(
        'companies/<pk>/areas/',
        views.AreasByCompanyList.as_view(),
        name='company-areas'
    ),
    path(
        'companies/<pk>/employees/',
        views.EmployeesByCompanyList.as_view(),
        name='company-employees'
    ),
    path(
        'areas/(<pk>/employees/',
        views.EmployeesByAreaList.as_view(),
        name='area-employees'
    ),
    path('', include(router.urls)),
]
