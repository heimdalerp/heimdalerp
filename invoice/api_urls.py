from django.urls import include, path
from invoice import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('fiscalpositions', views.FiscalPositionViewSet)
router.register('contacts', views.ContactInvoiceViewSet)
router.register('companies', views.CompanyInvoiceViewSet)
router.register('vats', views.VATViewSet)
router.register('products', views.ProductViewSet)
router.register('invoicelines', views.InvoiceLineViewSet)
router.register('invoicetypes', views.InvoiceTypeViewSet)
router.register('invoices', views.InvoiceViewSet)
router.register(
    'fiscalpositionshaveinvoicetypesallowed',
    views.FiscalPositionHasInvoiceTypeAllowedViewSet,
    basename='fiscalpositionhasinvoicetypeallowed'
)


app_name = 'invoice'
urlpatterns = [
    path(
        'companies/<pk>/products/',
        views.ProductsByCompanyList.as_view(),
        name='companyinvoice-products'
    ),
    path(
        'companies/<pk>/invoices/',
        views.InvoicesByCompanyList.as_view(),
        name='companyinvoice-invoices'
    ),
    path(
        'contacts/<pk>/invoices/',
        views.InvoicesByContactList.as_view(),
        name='contactinvoice-invoices'
    ),
    path(
        'products/<pk>/invoicelines/',
        views.InvoiceLinesByProductList.as_view(),
        name='product-invoicelines'
    ),
    path(
        'vats/<pk>/products/',
        views.ProductsByVATList.as_view(),
        name='vat-products'
    ),
    path(
        'fiscalpositions/<pk>/companies/',
        views.CompaniesByFiscalPositionList.as_view(),
        name='fiscalposition-companies'
    ),
    path(
        'fiscalpositions/<pk>/contacts/',
        views.ContactsByFiscalPositionList.as_view(),
        name='fiscalposition-contacts'
    ),
    path(
        'invoicetypes/<pk>/invoices',
        views.InvoicesByInvoiceTypeList.as_view(),
        name='invoicetype-invoices'
    ),
    path(
        'invoicetypes/bills/',
        views.InvoiceTypesByBillClassList.as_view(),
        name='invoicetype-bills'
    ),
    path(
        'invoicetypes/debits/',
        views.InvoiceTypesByDebitClassList.as_view(),
        name='invoicetype-debits'
    ),
    path(
        'invoicetypes/credits/',
        views.InvoiceTypesByCreditClassList.as_view(),
        name='invoicetype-credits'
    ),
    path('', include(router.urls)),
]
