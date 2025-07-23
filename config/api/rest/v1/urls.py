# config/api/rest/v1/urls.py

from django.urls import path, include

urlpatterns = [
    path('auth/', include('config.api.rest.v1.user_auth.urls')),
]
