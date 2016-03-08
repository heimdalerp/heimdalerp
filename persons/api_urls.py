from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from persons import views

router = DefaultRouter()
router.register(r'phonenumbers', views.PhoneNumberViewSet)
router.register(r'extraemailaddresses', views.ExtraEmailAddressViewSet)
router.register(r'physicaladdresses', views.PhysicalAddressViewSet)
router.register(r'companies', views.CompanyViewSet)

app_name = 'persons'
urlpatterns = [
    url(r'^', include(router.urls)),
]
