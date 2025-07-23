from config.api.rest.v1.user_auth.views import RegisterAPIView
from django.urls import path

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
]
