from rest_framework import  serializers
from store.models import Product,Category,Inventory,ProductImage,Rating

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        reads_only_fields = ["created_at","updated_at"]


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"
        reads_only_fields = ["created_at","updated_at","id"]

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

 


