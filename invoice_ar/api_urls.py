from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from invoice_ar import views

router = DefaultRouter()
router.register(r'clients', views.ClientARViewSet)
router.register(r'companies', views.CompanyInvoiceARViewSet)

app_name = 'invoice_ar'
urlpatterns = [
    url(r'^', include(router.urls)),
]
