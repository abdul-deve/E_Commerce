from config.api.rest.v1.store.serializers.serializers import (EmployeeSerializer,
                                                              ProductSerializer,
                                                              CategorySerializer)
from store.models import Employee,Product,Category
from store.permissions import PositionBasedPermission,EmployeeManagePermission

from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth import get_user_model

User = get_user_model()


from rest_framework import status
from rest_framework.response import Response
from django.db import transaction

class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [EmployeeManagePermission]
    authentication_classes = [BasicAuthentication]
    search_fields = ['user__username', 'user__email', 'position']
    ordering_fields = ['user__username', 'position']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.save()
            data = {
                "message": "Employee successfully created",
                "employee": {
                    "name": serializer.validated_data.get("name"),
                    "position":serializer.validated_data.get("position"),
                }
            }

        return Response(data, status=status.HTTP_201_CREATED)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class =  ProductSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [PositionBasedPermission]

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class =  CategorySerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [PositionBasedPermission]






