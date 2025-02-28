from rest_framework.permissions import BasePermission
from petitions.models import Petition

class CanViewPetition(BasePermission):
    """Permiso para permitir acceso a peticiones según el grupo."""

    def has_object_permission(self, request, view, obj):
        """Verifica si el usuario tiene acceso a la petición."""

        user = request.user

        if user.groups.filter(name="Admin").exists():
            return True  # Admins pueden ver todas las peticiones

        if user.groups.filter(name="Manager").exists():
            return (
                obj.department == user.human_resource.department
            )  # Managers ven su departamento

        if (user.groups.filter(name="Employee").exists()):
            return obj.user == user # Employees y Clients solo ven sus propias peticiones

        if user.groups.filter(name="Client").exists():
            # 🔥 Verificar si el cliente tiene varias empresas
            client_companies = user.human_resource.client_companies.values_list("company", flat=True)
            if client_companies.exists():
                return obj.company_id in client_companies
            return obj.company == user.human_resource.company
        
        return False  # Si no pertenece a un grupo válido, no tiene acceso


class IsAdmin(BasePermission):
    """Permiso que permite acceso solo a usuarios del grupo Admin."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Admin").exists()


class IsManager(BasePermission):
    """Permiso que permite acceso solo a usuarios del grupo Manager."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Manager").exists()


class IsEmployee(BasePermission):
    """Permiso que permite acceso solo a usuarios del grupo Employee."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Employee").exists()


class IsClient(BasePermission):
    """Permiso que permite acceso solo a usuarios del grupo Client."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Client").exists()
