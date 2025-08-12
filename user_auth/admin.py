from django.contrib import admin
from .models import User,PendingUser

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id","email","name"]
@admin.register(PendingUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email","username"]
