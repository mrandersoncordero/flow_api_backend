"""Department views."""

# Django REST Framework
from rest_framework import viewsets

# Models
from tasks.models import Department

# Serializers
from tasks.serializers import DeparmentSerializer


class DepartmentViewSet(viewsets.ModelViewSet):

    queryset = Department.objects.all()
    serializer_class = DeparmentSerializer