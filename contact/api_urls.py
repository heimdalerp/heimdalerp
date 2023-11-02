from contact import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('contacts', views.ContactViewSet)

app_name = 'contact'
urlpatterns = [
    path(
        'companies/<pk>/contacts/',
        views.ContactsByCompanyList.as_view(),
        name='company-contacts'
    ),
    path('', include(router.urls)),
]
