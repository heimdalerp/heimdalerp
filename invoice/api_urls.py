from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from invoice import views


router = DefaultRouter()
router.register(r'fiscalpositions', views.FiscalPositionViewSet)
router.register(r'companies', views.CompanyInvoiceViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'vats', views.VATViewSet)
router.register(r'invoiceproducts', views.InvoiceProductViewSet)
router.register(r'invoicelines', views.InvoiceLineViewSet)
router.register(r'invoices', views.InvoiceViewSet)

app_name = 'invoice'
urlpatterns = [
    url(r'^', include(router.urls)),
]

