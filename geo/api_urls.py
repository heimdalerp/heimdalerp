from django.urls import include, path
from geo import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('alternativenames', views.AlternativeNameViewSet)
router.register('localities', views.LocalityViewSet)
router.register('regions', views.RegionViewSet)
router.register('countries', views.CountryViewSet)

app_name = 'geo'
urlpatterns = [
    path(
        'countries/<pk>/regions/',
        views.RegionsByCountryList.as_view(),
        name='country-regions'
    ),
    path(
        'countries/<pk>/localities/',
        views.LocalitiesByCountryList.as_view(),
        name='country-localities'
    ),
    path(
        'regions/<pk>/localities/',
        views.LocalitiesByRegionList.as_view(),
        name='region-localities'
    ),
    path('', include(router.urls)),
]
