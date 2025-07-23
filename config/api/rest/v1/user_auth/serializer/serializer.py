from rest_framework import serializers

from django.contrib.auth import authenticate,get_user_model
from user_auth.models import PendingUser

User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingUser
        fields = "__all__"
        read_only_fields =  ["created_at","updated_at"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")
        password = attrs.get("password")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "This email is already registered."})

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})

        if len(password) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})

        return attrs

    def create(self, **validated_data):
        pending_user = PendingUser.objects.create(**validated_data)
        return pending_user



class LoginSerializer(serializers.Serializer):
   email = serializers.EmailField(allow_null=False,allow_blank=False)
   password = serializers.CharField(max_length=250,allow_null=False,allow_blank=False)

   def validate(self, attrs):
       email = attrs.get("email")
       password = attrs.get("password")

       user = authenticate(username=email,password=password)
       if not user:
            raise serializers.ValidationError("Invalid credentials")

       attrs["user"] = user
       return attrs






