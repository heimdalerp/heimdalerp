from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import urls as restframework_urls
from rest_framework_jwt.views import obtain_jwt_token

from . import api_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(
        r'^api-auth/',
        include(restframework_urls, namespace='rest_framework')
    ),
    url(
        r'^api-token-auth/',
        obtain_jwt_token
    ),
    url(r'^api/', include(api_urls, namespace='api')),
]
