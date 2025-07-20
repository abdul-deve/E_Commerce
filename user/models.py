from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import TimeStamp
import uuid





class User(AbstractUser,TimeStamp):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4())
    email = models.EmailField(max_length=250,unique=True,db_index=True)
    user_name = models.CharField(max_length=250,unique=True,db_index=True)


class Profile(TimeStamp):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name  = models.CharField(max_length=250)
    profile_pic = models.ImageField(null=True,blank=True)
    phone_number = models.PositiveSmallIntegerField(max_length=20,null=True,blank=True,unique=True)






