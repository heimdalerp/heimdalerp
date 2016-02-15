from django.conf.urls import url, include

from persons import api_urls as persons_urls

urlpatterns = [
    url(
        r'^persons/',
        include(persons_urls, namespace='persons')
    ),
]    
