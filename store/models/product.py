from django.db import models
from store.models.category import Category,get_main_category
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator,MaxValueValidator
User = get_user_model()

class Product(models.Model):
    id =  models.UUIDField(primary_key=True,editable=False,default=uuid4)
    name = models.CharField(max_length=255,db_index=True)
    price = models.FloatField()
    category = models.ForeignKey(Category,on_delete=models.SET(get_main_category), related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='product_images/')

class Rating(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4,db_index=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,db_index=True,related_name="user")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    rating  = models.IntegerField(validators= [MinValueValidator(1),MaxValueValidator(5)],null=True,blank=True,default=1)
    rated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("product","user")

    def __str__(self):
        return f"Name : {self.user.username}, Product : {self.product.name},Rating:{self.rating}"





