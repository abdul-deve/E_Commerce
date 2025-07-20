from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import TimeStamp,UniqueID





class User(AbstractUser,TimeStamp,UniqueID):
    email = models.EmailField(max_length=250,unique=True,db_index=True)
    user_name = models.CharField(max_length=250,unique=True,db_index=True)


class Profile(TimeStamp,UniqueID):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name  = models.CharField(max_length=250)
    profile_pic = models.ImageField(null=True,blank=True)
    phone_number = models.PositiveSmallIntegerField(max_length=20,null=True,blank=True,unique=True)

class Address(TimeStamp,UniqueID):
    user = models.OneToOneField(User,on_delete=models.CASCADE)









