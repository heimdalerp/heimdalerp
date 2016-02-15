from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from persons import views


router = DefaultRouter()
router.register(r'phonenumbers', views.PhoneNumberViewSet)
router.register(r'extraemails', views.ExtraEmailAddressViewSet)
router.register(r'physicaladdresses', views.PhysicalAddressViewSet)

app_name = 'persons'
urlpatterns = [
    url(r'^', include(router.urls)),
]

