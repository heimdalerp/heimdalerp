from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from geo import views

router = DefaultRouter()
router.register(r'cities', views.CityModelViewSet)
router.register(r'regions', views.RegionModelViewSet)
router.register(r'countries', views.CountryModelViewSet)

app_name = 'geo'
urlpatterns = [
    url(r'^', include(router.urls)),
]
