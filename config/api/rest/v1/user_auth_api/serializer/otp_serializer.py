from rest_framework import serializers

from user_auth.models import PendingUser

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def create(self, validated_data):
        return super().create

