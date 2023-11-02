from django.urls import include, path
from persons import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('physicaladdresses', views.PhysicalAddressViewSet)
router.register('companies', views.CompanyViewSet)

app_name = 'persons'
urlpatterns = [
    path('', include(router.urls)),
]
