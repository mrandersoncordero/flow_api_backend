"""Tasks views."""

# Django
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date

# Django REST Framework
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

# Models
from tasks.models import Task, TaskStatus

# Serializers
from tasks.serializers import TaskSerializer, TaskStatusModelSerializer


class TaskStatusAPIView(APIView):
    """Vista Basada en clases para manejar POST, GET, PUT, PATCH y DELETE."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        # Si se pasa un ID (pk) se retorna un status especifico
        if pk:
            task_status = get_object_or_404(TaskStatus, pk=pk)
            serializer = TaskStatusModelSerializer(task_status)
            return Response(serializer.data)

        task_status = TaskStatus.objects.all()
        serializer = TaskStatusModelSerializer(task_status, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Crear un nuevo status
        serializer = TaskStatusModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response(
            TaskStatusModelSerializer(task).data, status=status.HTTP_201_CREATED
        )

    def put(self, request, pk):
        # Actualizar un status
        task_status = get_object_or_404(TaskStatus, pk=pk)
        serializer = TaskStatusModelSerializer(task_status, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Eliminar un status
        task_status = get_object_or_404(TaskStatus, pk=pk)
        task_status.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Filtrar por parametros de la URL"""
        queryset = Task.objects.all()
        company = self.request.query_params.get('company', None)
        department = self.request.query_params.get('department', None)
        date_from = self.request.query_params.get('date_from', None)
        date_until = self.request.query_params.get('date_until', None)

        if company:
            queryset = queryset.filter(company=company)
        if department:
            queryset = queryset.filter(department=department)
        
        if date_from:
            date_from = parse_date(date_from)
            if date_from:
                queryset = queryset.filter(created__gte=date_from)

        if date_until:
            date_until = parse_date(date_until)
            if date_until:
                queryset = queryset.filter(created__lte=date_until)
        
        return queryset
