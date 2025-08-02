from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import ValidationError

from user_auth.models import PendingUser
from config.api.rest.v1.user_auth_api.serializer.otp_serializer import OTPVerificationSerializer
from config.api.rest.v1.user_auth_api.views.user_vewis import get_tokens_for_user


@api_view(http_method_names=['POST'])
def verify_otp(request):
    serializer = OTPVerificationSerializer(data=request.data,context={"context":request})
    email = request.data.get("email")
    otp = request.data.get("otp")
    try:
        pending_user = PendingUser.objects.get(email=email)
    except PendingUser.DoesNotExist:
        raise ValidationError("Invalid credentials")
    if not pending_user.validate_otp(otp):
        raise ValidationError("Invalid OTP")
    user = pending_user.create_real_user()
    print(pending_user.password)
    pending_user.delete()
    tokens = get_tokens_for_user(user)
    if serializer.is_valid():
        serializer.save()
        data = {
            "Tokens" : tokens,
            "Message" : "OTP verified",
        }
        return Response((data, status.HTTP_200_OK))
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
