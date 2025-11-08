from django.contrib import admin
from apps.users.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'name', 'last_name')