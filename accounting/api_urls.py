from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from accounting import views

router = DefaultRouter()
router.register(r'ledgers', views.LedgerViewSet)
router.register(r'accounts', views.AccountViewSet)
router.register(r'accountsubtypes', views.AccountSubtypeViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'payments', views.PaymentViewSet)

app_name = 'accounting'
urlpatterns = [
    url(
        r'^accounts/(?P<pk>\d+)/payments/$',
        views.PaymentsByAccountList.as_view(),
        name='account-payments'
    ),
    url(
        r'^contacts/(?P<pk>\d+)/payments/$',
        views.PaymentsByContactList.as_view(),
        name='contact-payments'
    ),
    url(
        r'^company/(?P<pk>\d+)/ledgers/$',
        views.LedgersByCompanyList.as_view(),
        name='company-ledgers'
    ),
    url(
        r'^company/(?P<pk>\d+)/payments/$',
        views.PaymentsByCompanyList.as_view(),
        name='company-payments'
    ),
    url(
        r'^ledgers/(?P<pk>\d+)/accounts/$',
        views.AccountsByLedgerList.as_view(),
        name='ledger-accounts'
    ),
    url(
        r'^accountsubtypes/(?P<pk>\d+)/accounts/$',
        views.AccountsByAccountSubtypeList.as_view(),
        name='accountsubtype-accounts'
    ),
    url(
        r'^accounts/(?P<pk>\d+)/transactions/$',
        views.TransactionsByAccountList.as_view(),
        name='account-transactions'
    ),
    url(r'^', include(router.urls)),
]
