from django.conf.urls import include, url
from geo import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'alternativenames', views.AlternativeNameViewSet)
router.register(r'localities', views.LocalityViewSet)
router.register(r'regions', views.RegionViewSet)
router.register(r'countries', views.CountryViewSet)

app_name = 'geo'
urlpatterns = [
    url(
        r'^countries/(?P<pk>\d+)/regions/$',
        views.RegionsByCountryList.as_view(),
        name='country-regions'
    ),
    url(
        r'^countries/(?P<pk>\d+)/localities/$',
        views.LocalitiesByCountryList.as_view(),
        name='country-localities'
    ),
    url(
        r'^regions/(?P<pk>\d+)/localities/$',
        views.LocalitiesByRegionList.as_view(),
        name='region-localities'
    ),
    url(r'^', include(router.urls)),
]
