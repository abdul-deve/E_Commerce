# Django Built-IN Methods & Classes & Modules
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager,PermissionsMixin
from django.core.exceptions import ValidationError
from common.otp import generate_otp
from common.emails import opt_verification_email

#Thrid-Party Libraries
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField

#Projects Methods,Modules,Classes,
from common.models import TimeStampUniqueID

class UserManager(BaseUserManager):

    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValidationError("Invalid credentials")
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        if not email:
            raise ValidationError("Invalid credentials")
        return self.create_user(email,password,**extra_fields)


class PendingUser(TimeStampUniqueID,models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=250)
    username = models.CharField(max_length=250)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)

    def set_otp(self):
        self.otp = generate_otp()
        self.save()
        opt_verification_email(user_email=self.email,user_name=self.username)

    def validate_otp(self,entered_otp):
        if self.otp == entered_otp:
            self.is_verified = True
            self.save()
            return  True
        return  False
    def delete_obj(self):
        self.delete()
    




class User(TimeStampUniqueID,AbstractUser,PermissionsMixin):
    name = models.CharField(max_length=250)
    email = models.EmailField(db_index=True,unique=True)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=250,unique=True,db_index=True)
    objects = UserManager()
    USERNAME_FIELD =  "email"
    REQUIRED_FIELDS = ()
    def save(self,*args,**kwargs):
        self.email = self.email.strip().lower()
        return  super().save(*args,**kwargs)

    def get_email(self):
        return self.email
    class Meta:
        abstract = False


def validate_image(image):
    max_file_size = 1 * 1024 * 1024  # 1MB
    if image.size > max_file_size:
        raise ValidationError("File too large! Should be under 1MB.")
    img = Image.open(image)
    if img.width > 800 or img.height > 800:
        raise ValidationError("Image dimensions should not exceed 800x800 pixels.")


class UserProfile(TimeStampUniqueID,models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,db_index=True,editable=False,related_name="user_profile")
    name = models.CharField(max_length=250)
    phone_number = PhoneNumberField(region="PK",unique=True,db_index=True)
    profile_pic = models.ImageField(validators=[validate_image])


class Address(TimeStampUniqueID,models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    country = models.CharField(max_length=250,db_index=True)
    state = models.CharField(max_length=250,db_index=True)
    city= models.CharField(max_length=250,db_index=True)
    street = models.CharField(max_length=250,db_index=True,null=True,blank=True)

    def __str__(self):
        return f" Country: {self.country} State: {self.state} City: {self.city} Street:{self.street} "










