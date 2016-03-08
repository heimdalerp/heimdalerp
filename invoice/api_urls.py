from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from invoice import views

router = DefaultRouter()
router.register(r'fiscalpositions', views.FiscalPositionViewSet)
router.register(r'companies', views.CompanyInvoiceViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'vats', views.VATViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'invoicelines', views.InvoiceLineViewSet)
router.register(r'invoices', views.InvoiceViewSet)

app_name = 'invoice'
urlpatterns = [
    url(
        r'^companies/(?P<pk>\d+)/clients/$',
        views.ClientsByCompanyList.as_view(),
        name='company-clients'
    ),
    url(
        r'^companies/(?P<pk>\d+)/products/$',
        views.ProductsByCompanyList.as_view(),
        name='company-products'
    ),
    url(
        r'^companies/(?P<pk>\d+)/invoices/$',
        views.InvoicesByCompanyList.as_view(),
        name='company-invoices'
    ),
    url(
        r'^clients/(?P<pk>\d+)/invoices/$',
        views.InvoicesByClientList.as_view(),
        name='client-invoices'
    ),
    url(
        r'^clients/(?P<pk>\d+)/companies/$',
        views.CompaniesByClientList.as_view(),
        name='client-companies'
    ),
    url(
        r'^products/(?P<pk>\d+)/invoicelines/$',
        views.InvoiceLinesByProductList.as_view(),
        name='product-invoicelines'
    ),
    url(
        r'^vats/(?P<pk>\d+)/products/$',
        views.ProductsByVATList.as_view(),
        name='vat-products'
    ),
    url(
        r'^fiscalpositions/(?P<pk>\d+)/companies/$',
        views.CompaniesByFiscalPositionList.as_view(),
        name='fiscalposition-companies'
    ),
    url(
        r'^fiscalpositions/(?P<pk>\d+)/clients/$',
        views.ClientsByFiscalPositionList.as_view(),
        name='fiscalposition-clients'
    ),
    url(r'^', include(router.urls)),
]
