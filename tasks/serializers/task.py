"""Task serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from tasks.models import Task, Department, TaskStatus
from users.models import User


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            "id",
            "user",
            "title",
            "description",
            "department",
            "company",
            "status",
            "hours",
            "created",
            "modified",
        ]
        read_only_fields = ["created", "modified"]


class TaskStatusModelSerializer(serializers.ModelSerializer):
    """Tasks status model serializer."""

    class Meta:
        """Meta class."""
        model = TaskStatus
        fields = '__all__'