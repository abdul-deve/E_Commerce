from django.contrib import admin
from models import User,Profile,Address

@admin.register(User)
class UserAdminPanel(admin.ModelAdmin):
    list_display = "__all__"
    search_fields = ('email', 'username')

