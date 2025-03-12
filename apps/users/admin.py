"""Tasks admin."""

# Django
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin

# Models
from .models import User, HumanResource, ClientCompany


class UserAdmin(BaseUserAdmin):
    """Add profile admin to base user admin."""

    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_verified",
        "created",
    ]
    list_editable = ["is_verified"]
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["-created"]


class ClientCompanyInline(admin.TabularInline):
    """Permite agregar empresas adicionales a un Cliente en HumanResourceAdmin."""

    model = ClientCompany
    extra = 1  # 🔥 Muestra un campo adicional en blanco
    verbose_name = "Empresa Adicional"
    verbose_name_plural = "Empresas Adicionales"

    def has_add_permission(self, request, obj=None):
        """Solo permite agregar si el usuario es un `Client`."""
        if obj and obj.user.groups.filter(name="Client").exists():
            return True
        return False

    def has_change_permission(self, request, obj=None):
        """Solo permite editar si el usuario es un `Client`."""
        if obj and obj.user.groups.filter(name="Admin").exists():
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        """Solo permite eliminar si el usuario es un `Client`."""
        if obj and obj.user.groups.filter(name="Admin").exists():
            return True
        return False


class HumanResourceAdmin(admin.ModelAdmin):
    """Admin para HumanResource."""

    list_display = ["user", "company", "department"]
    list_filter = ["company", "department"]
    search_fields = ["user__email", "user__first_name", "user__last_name"]

    inlines = [
        ClientCompanyInline
    ]  # 🔥 Agrega la relación de empresas solo si el usuario es Client


admin.site.register(HumanResource, HumanResourceAdmin)
admin.site.register(User, UserAdmin)
