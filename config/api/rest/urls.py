# config/api/urls.py

from django.urls import path, include

urlpatterns = [
    path('v1/', include('config.api.rest.v1.urls')),
]
