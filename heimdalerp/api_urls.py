from django.conf.urls import url, include

from cities_light.contrib import restframework3 as geo_urls
from persons import api_urls as persons_urls

urlpatterns = [
    url(
        r'^geo/',
        include(geo_urls, namespace='geo')
    ),
    url(
        r'^persons/',
        include(persons_urls, namespace='persons')
    ),
]    
