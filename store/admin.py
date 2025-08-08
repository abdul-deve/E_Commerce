from django.contrib import admin
from .models import Product, Category, Inventory,ProductImage

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Inventory)
admin.site.register(ProductImage)
