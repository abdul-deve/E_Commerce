from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import ValidationError
from rest_framework.views import APIView

from django.contrib.auth import get_user_model

from user_auth.models import PendingUser


User = get_user_model()


class RegisterAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            pending_user = PendingUser.objects.get(email=email)
        except PendingUser.DoesNotExist:
            raise ValidationError("Invalid credentials")

        if not pending_user.is_verified:
            raise ValidationError("OTP is not verified")

        real_user = self.create_user_by_pending_user(pending_user)

        data = {
            "username": real_user.username,
            "email": real_user.email,
        }
        return Response({"message": "User successfully registered", "data": data}, status=status.HTTP_201_CREATED)

    @staticmethod
    def create_user_by_pending_user(pending_user):
        if not pending_user.is_verified:
            raise ValidationError("Invalid credentials")

        real_user = User.objects.create_user(
            email=pending_user.email,
            password=pending_user.password,
            username=pending_user.username
        )
        pending_user.delete_obj()
        return real_user






