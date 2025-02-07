"""Department views."""

# Django
from django.db.models import ProtectedError

# Django REST Framework
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Models
from tasks.models import Department

# Serializers
from tasks.serializers import DeparmentSerializer


class DepartmentViewSet(viewsets.ModelViewSet):

    queryset = Department.objects.all()
    serializer_class = DeparmentSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Filtrar por parametros de la URL"""
        queryset = Department.objects.all()
        name = self.request.query_params.get('name', None)
        description = self.request.query_params.get('description', None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if description:
            queryset = queryset.filter(description__icontains=description)
        
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        department = self.get_object()
        try:
            self.perform_destroy(department)
        except ProtectedError:
            return Response(
                {"detail": "Cannot delete this department as it has associated tasks."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
    