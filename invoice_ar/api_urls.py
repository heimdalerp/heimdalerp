from django.urls import include, path
from invoice_ar import views
from rest_framework.routers import DefaultRouter
from rest_framework_proxy.views import ProxyView

router = DefaultRouter()
router.register('contacts', views.ContactInvoiceARViewSet)
router.register('companies', views.CompanyInvoiceARViewSet)
router.register('webservicesessions', views.WebServiceSessionViewSet)
router.register('pointsofsalear', views.PointOfSaleARViewSet)
router.register('concepttypes', views.ConceptTypeViewSet)
router.register('invoices', views.InvoiceARViewSet)
router.register(
    'invoiceshavevatsubtotals',
    views.InvoiceARHasVATSubtotalViewSet
)

app_name = 'invoice_ar'
urlpatterns = [
    path(
        'afipws/cuit/<cuit>/',
        ProxyView.as_view(source='sr-padron/v2/persona/%(cuit)s'),
        name='afipws-cuit'
    ),
    path(
        'afipws/dni/<dni>/',
        ProxyView.as_view(source='sr-padron/v2/personas/%(dni)s'),
        name='afipws-dni'
    ),
    path(
        'concepttypes/<pk>/invoices/',
        views.InvoicesByConceptTypeList.as_view(),
        name='concepttype-invoices'
    ),
    path(
        'invoices/<pk>/relatedinvoices/',
        views.InvoicesByRelatedInvoiceList.as_view(),
        name='invoice-relatedinvoices'
    ),
    path(
        'contacts/<pk>/invoices/',
        views.InvoicesByContactList.as_view(),
        name='contactinvoicear-invoices'
    ),
    path(
        'companies/<pk>/invoices/',
        views.InvoicesByCompanyList.as_view(),
        name='companyinvoicear-invoices'
    ),
    path(
        'companies/<pk>/webservicesessions/',
        views.WebServiceSessionsByCompanyList.as_view(),
        name='companyinvoicear-webservicesessions'
    ),
    path(
        'pointsofsalear/<pk>/invoices/',
        views.InvoicesByPointOfSaleARList.as_view(),
        name='pointofsalear-invoices'
    ),
    path(
        'invoicetypes/<pk>/invoices',
        views.InvoicesByInvoiceTypeList.as_view(),
        name='invoicetype-invoices'
    ),
    path('', include(router.urls)),
]
