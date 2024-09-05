"""Department views."""

# Django REST Framework
from rest_framework import viewsets
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
    