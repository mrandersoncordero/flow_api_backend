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
            "status",
            "hours",
            "created",
            "modified",
        ]
        read_only_fields = ["created", "modified"]

    def create(self, data):
        task = Task.objects.create(
            user=data["user"],
            title=data["title"],
            description=data["description"],
            department=data["department"],
            status=data["status"],
            hours=data["hours"],
        )

        return task
