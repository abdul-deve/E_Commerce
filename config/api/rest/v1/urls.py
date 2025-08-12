# config/api/rest/v1/urls.py
from django.urls import path, include
from dj_rest_auth.views import PasswordResetConfirmView



urlpatterns = [
    path('auth/', include('config.api.rest.v1.user_auth_api.urls')),
    path('store/', include('config.api.rest.v1.store.urls')),
    path('auth/', include('dj_rest_auth.urls')),
path(
        'api/v1/auth/password/reset/confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),


]
