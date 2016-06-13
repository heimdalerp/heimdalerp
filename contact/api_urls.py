from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from contact import views

router = DefaultRouter()
router.register(r'contacts', views.ContactViewSet)

app_name = 'contact'
urlpatterns = [
    url(
        r'^companies/(?P<pk>\d+)/contacts/$',
        views.ContactsByCompanyList.as_view(),
        name='company-contacts'
    ),
    url(r'^', include(router.urls)),
]
