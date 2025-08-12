from rest_framework.generics import RetrieveAPIView,CreateAPIView
from config.api.rest.v1.store.serializers.user_end_serializer import RateSerializer
from store.models import Product

class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
