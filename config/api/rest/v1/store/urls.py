
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet,CategoryViewSet
router = DefaultRouter()
router.register("product",ProductViewSet,basename="products")
router.register("category",CategoryViewSet,basename="category")

urlpatterns = [
    path('', include(router.urls)),

]
