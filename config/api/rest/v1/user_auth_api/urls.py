from config.api.rest.v1.user_auth_api.views.user_vewis import RegisterAPI
from config.api.rest.v1.user_auth_api.views.otp_views import  verify_otp
from config.api.rest.v1.user_auth_api.views.social_views import GoogleLogin,SocialLoginView

from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('verify-otp/', verify_otp, name='verify-otp'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('social/', SocialLoginView.as_view(), name='social_login'),
    path('social/google/', GoogleLogin.as_view(), name='google_login'),
]
