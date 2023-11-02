from accounting import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('ledgers', views.LedgerViewSet)
router.register('accounts', views.AccountViewSet)
router.register('transactions', views.TransactionViewSet)
router.register('payments', views.PaymentViewSet)
router.register('companies', views.CompanyAccountingViewSet)

app_name = 'accounting'
urlpatterns = [
    path(
        'contacts/<pk>/payments/',
        views.PaymentsByContactList.as_view(),
        name='contact-payments'
    ),
    path(
        'company/<pk>/ledgers/',
        views.LedgersByCompanyList.as_view(),
        name='company-ledgers'
    ),
    path(
        'company/(<pk>/payments/',
        views.PaymentsByCompanyList.as_view(),
        name='company-payments'
    ),
    path(
        'ledgers/<pk>/accounts/',
        views.AccountsByLedgerList.as_view(),
        name='ledger-accounts'
    ),
    path(
        'accounts/<pk>/transactions/',
        views.TransactionsByAccountList.as_view(),
        name='account-transactions'
    ),
    path('', include(router.urls)),
]
