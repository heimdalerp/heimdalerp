from django.urls import include, path
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

from heimdalerp import api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'api-token-auth/',
        obtain_jwt_token
    ),
    path('api/', include(api_urls)),
]
