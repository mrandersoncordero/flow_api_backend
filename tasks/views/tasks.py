"""Tasks views."""

# Django REST Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Models
from tasks.models import Task, Department, TaskStatus
from users.models import User

# Serializers
from tasks.serializers import TaskSerializer


@api_view(["GET"])
def list_tasks(request):
    """List circles."""
    # import ipdb; ipdb.set_trace()
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def create_task(request):
    """Create task"""
    serializer = TaskSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    task = serializer.save()
    return Response(TaskSerializer(task).data)
