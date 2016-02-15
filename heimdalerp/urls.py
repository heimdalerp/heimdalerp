from django.conf.urls import url, include
from django.contrib import admin

from . import api_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(
        r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
    url(
        r'^api-token-auth/',
        'rest_framework_jwt.views.obtain_jwt_token'
    ),
    url(r'^api/', include(api_urls, namespace='api')),
]
