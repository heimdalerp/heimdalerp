from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from rest_framework_proxy.views import ProxyView

from invoice_ar import views

router = DefaultRouter()
router.register(r'contacts', views.ContactInvoiceARViewSet)
router.register(r'companies', views.CompanyInvoiceARViewSet)

app_name = 'invoice_ar'
urlpatterns = [
    url(
        r'^afipws/cuit/(?P<cuit>[0-9]+)/$',
        ProxyView.as_view(source='sr-padron/v2/persona/%(cuit)s'),
        name='afipws-cuit'
    ),
    url(
        r'^afipws/dni/(?P<dni>[0-9]+)/$',
        ProxyView.as_view(source='sr-padron/v2/personas/%(dni)s'),
        name='afipws-dni'
    ),
    url(r'^', include(router.urls)),
]
