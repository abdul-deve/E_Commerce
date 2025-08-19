from django.urls import path, include
from .views.views import EmployeeViewSet,ProductViewSet,CategoryViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("employee",EmployeeViewSet,"employees")
router.register("category",CategoryViewSet,"category")
router.register("product",ProductViewSet,"product")
urlpatterns = [
    path("",include(router.urls))




]
