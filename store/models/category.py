from django.db import models
from uuid import uuid4

def get_main_category(self):
    return Category.objects.filter(name="Main").first() or Category.objects.create(name="Main")



class Category(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4)
    name = models.CharField(max_length=255,db_index=True)
    category = models.ForeignKey("self",on_delete=models.SET_NULL,null=True,blank=True, related_name="sub_categories")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)


    def __str__(self):
        return f"Name : {self.name}"
