from django.conf.urls import include, url
from invoice_ar import views
from rest_framework.routers import DefaultRouter
from rest_framework_proxy.views import ProxyView

router = DefaultRouter()
router.register(r'contacts', views.ContactInvoiceARViewSet)
router.register(r'companies', views.CompanyInvoiceARViewSet)
router.register(r'webservicesessions', views.WebServiceSessionViewSet)
router.register(r'pointsofsalear', views.PointOfSaleARViewSet)
router.register(r'concepttypes', views.ConceptTypeViewSet)
router.register(r'invoices', views.InvoiceARViewSet)
router.register(
    r'invoiceshavevatsubtotals',
    views.InvoiceARHasVATSubtotalViewSet
)

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
    url(
        r'^concepttypes/(?P<pk>\d+)/invoices/$',
        views.InvoicesByConceptTypeList.as_view(),
        name='concepttype-invoices'
    ),
    url(
        r'^contacts/(?P<pk>\d+)/invoices/$',
        views.InvoicesByContactList.as_view(),
        name='contactinvoicear-invoices'
    ),
    url(
        r'^companies/(?P<pk>\d+)/invoices/$',
        views.InvoicesByCompanyList.as_view(),
        name='companyinvoicear-invoices'
    ),
    url(
        r'^companies/(?P<pk>\d+)/webservicesessions/$',
        views.WebServiceSessionsByCompanyList.as_view(),
        name='companyinvoicear-webservicesessions'
    ),
    url(
        r'^pointsofsalear/(?P<pk>\d+)/invoices/$',
        views.InvoicesByPointOfSaleARList.as_view(),
        name='pointofsalear-invoices'
    ),
    url(
        r'^invoicetypes/(?P<pk>\d+)/invoices$',
        views.InvoicesByInvoiceTypeList.as_view(),
        name='invoicetype-invoices'
    ),
    url(r'^', include(router.urls)),
]
