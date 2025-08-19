from rest_framework import serializers
from store.models import Product, Category, ProductImage,Employee

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        reads_only_fields = ["created_at", "updated_at"]


class ProductImageSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        min_length=1,
        max_length=4
    )

    def create(self, validated_data):
        product = validated_data['product']
        images = validated_data['images']

        product_images = [
            ProductImage(product=product, image=image)
            for image in images
        ]
        ProductImage.objects.bulk_create(product_images)
        return {"message" f"Images uploaded {len(product_images)}"}


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        min_length=1,
        max_length=4
    )

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        images = validated_data.pop('images')
        product = super().create(validated_data)
        image_payload = {
            "product": product.id,
            "images": images
        }
        image_serializer = ProductImageSerializer(data=image_payload)
        image_serializer.is_valid(raise_exception=True)
        image_serializer.save()
        return product



class EmployeeSerializer(serializers.Serializer):
    # User input fields (write-only)
    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(write_only=True)

    # Employee fields
    id = serializers.UUIDField(read_only=True)
    position = serializers.CharField()
    salary = serializers.IntegerField()
    joined_date = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return {
            "username": obj.user.username,
            "email": obj.user.email,
            "name": obj.user.name,
            "is_staff": obj.user.is_staff
        }

    def create(self, validated_data):
        # Extract user data
        user_data = {
            "email": validated_data.pop("email"),
            "username": validated_data.pop("username"),
            "name": validated_data.pop("name"),
            "password": make_password(validated_data.pop("password")),
            "is_staff": validated_data.pop("is_staff"),
        }
        employee_data = validated_data

        user, created = User.objects.update_or_create(
            username=user_data['username'],
            defaults={
                "email": user_data['email'],
                "name": user_data['name'],
                "password": user_data['password'],
                "is_staff": user_data['is_staff'],
            }
        )

        employee = Employee.objects.create(user=user, **employee_data)
        return employee









