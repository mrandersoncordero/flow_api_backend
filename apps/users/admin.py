"""Tasks admin."""

# Django
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

# Models
from .models import User

class UserAdmin(BaseUserAdmin):
    """Add profile admin to base user admin."""

    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'created']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-created']


admin.site.register(User, UserAdmin)