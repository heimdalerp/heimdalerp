from django.conf.urls import include, url
from persons import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'physicaladdresses', views.PhysicalAddressViewSet)
router.register(r'companies', views.CompanyViewSet)

app_name = 'persons'
urlpatterns = [
    url(r'^', include(router.urls)),
]
