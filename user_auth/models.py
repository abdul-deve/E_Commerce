from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from uuid import uuid4

from common.otp import generate_otp
from common.emails import opt_verification_email
from config.api.rest.v1.user_auth_api.email import send_welcome_email

from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField

class TimeStampUniqueID:
    id = models.UUIDField(primary_key=True,editable=False,default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True




class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValidationError("Invalid credentials")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not email:
            raise ValidationError("Invalid credentials")
        return self.create_user(email, password, **extra_fields)


class PendingUser(TimeStampUniqueID, models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=1000)
    username = models.CharField(max_length=250)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank=True, null=True)

    def set_otp(self):
        self.otp = generate_otp()
        self.created_at = timezone.now()
        self.save(update_fields=['otp', 'created_at'])
        opt_verification_email(user_email=self.email, user_name=self.username, otp=self.otp)

    def validate_otp(self, entered_otp):
        if self.created_at and timezone.now() - self.created_at > timedelta(minutes=5):
            return False
        if self.otp == entered_otp:
            self.is_verified = True
            self.save(update_fields=['is_verified'])
            return True
        return False

    def create_real_user(self):
        if not self.is_verified:
            raise ValidationError("OTP not Verified")
        user_model = get_user_model()
        real_user = user_model.objects.create_user(
            email=self.email,
            password=self.password,
            username=self.username,
        )
        real_user.save()
        return real_user

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        abstract = False


class User(TimeStampUniqueID, AbstractUser):
    name = models.CharField(max_length=250)
    email = models.EmailField(db_index=True, unique=True)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=250, unique=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    def save(self, *args, **kwargs):
        self.email = self.email.strip().lower()
        return super().save(*args, **kwargs)

    def get_email(self):
        return self.email

    class Meta:
        abstract = False


def validate_image(image):
    max_file_size = 1 * 1024 * 1024
    if image.size > max_file_size:
        raise ValidationError("File too large! Should be under 1MB.")
    img = Image.open(image)
    if img.width > 800 or img.height > 800:
        raise ValidationError("Image dimensions should not exceed 800x800 pixels.")


class UserProfile(TimeStampUniqueID, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True, editable=False,
                                related_name="user_profile")
    phone_number = PhoneNumberField(region="PK", unique=True, db_index=True)
    profile_pic = models.ImageField(validators=[validate_image])
    class Meta:
        abstract = False


class Address(TimeStampUniqueID, models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, editable=False, related_name="user_address")
    country = models.CharField(max_length=250, db_index=True)
    state = models.CharField(max_length=250, db_index=True)
    city = models.CharField(max_length=250, db_index=True)
    street = models.CharField(max_length=250, db_index=True, null=True, blank=True)

    class Meta:
        abstract = False

    def __str__(self):
        return f" Country: {self.country} State: {self.state} City: {self.city} Street:{self.street} "
