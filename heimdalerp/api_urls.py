from django.urls import include, path

from contact import api_urls as contact_urls
from hr import api_urls as hr_urls
from geo import api_urls as geo_urls
from invoice import api_urls as invoice_urls
from invoice_ar import api_urls as invoicear_urls
from persons import api_urls as persons_urls
from accounting import api_urls as accounting_urls


urlpatterns = [
    path(
        'geo/',
        include(geo_urls, namespace='geo')
    ),
    path(
        'persons/',
        include(persons_urls, namespace='persons')
    ),
    path(
        'contact/',
        include(contact_urls, namespace='contact')
    ),
    path(
        'hr/',
        include(hr_urls, namespace='hr')
    ),
    path(
        'invoice/',
        include(invoice_urls, namespace='invoice')
    ),
    path(
        'invoice_ar/',
        include(invoicear_urls, namespace='invoice_ar')
    ),
    path(
        'accounting/',
        include(accounting_urls, namespace='accounting')
    ),
]
