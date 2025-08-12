
from store.models import (Product,
                            Category,
                            Inventory,)

from config.api.rest.v1.store.serializers.admin_end__serializers import (CategorySerializer,
                                                                         ProductSerializer,
                                                                         InventorySerializer,
                                                                         ProductImageSerializer)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import  status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.response import Response



class CategoryViewSet(ModelViewSet):
    queryset =  Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes =  []
    authentication_classes =  []

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []
    authentication_classes = []


    def get_permissions(self):
        pass