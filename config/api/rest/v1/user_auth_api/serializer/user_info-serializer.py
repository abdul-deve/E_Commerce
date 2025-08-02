from rest_framework import serializers


from user_auth.models import UserProfile,Address

class UserInfoSerializer(serializers.ModelSerializer):
    class