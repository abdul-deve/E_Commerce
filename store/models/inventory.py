from django.db import models

from store.models.product import Product

class Inventory(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sold = models.IntegerField(default=0)
    availability = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def save(self,*args,**kwargs):
        self.sold = 0
        return super().save(*args,**kwargs)