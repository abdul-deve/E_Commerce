from store.models import Product,Rating

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Rating
        fields = "__all__"
        reads_only_fields = ["rated_at","id","user"]
