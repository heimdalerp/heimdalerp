from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from geo import views

router = DefaultRouter()
router.register(r'cities', views.CityModelViewSet)
router.register(r'regions', views.RegionModelViewSet)
router.register(r'countries', views.CountryModelViewSet)

app_name = 'geo'
urlpatterns = [
    url(
        r'^countries/(?P<geoname_id>\d+)/regions/$',
        views.RegionsByCountryList.as_view(),
        name='country-regions'
    ),
    url(
        r'^countries/(?P<geoname_id>\d+)/cities/$',
        views.CitiesByCountryList.as_view(),
        name='country-cities'
    ),
    url(
        r'^regions/(?P<geoname_id>\d+)/cities/$',
        views.CitiesByRegionList.as_view(),
        name='region-cities'
    ),
    url(r'^', include(router.urls)),
]
