"""Tasks views."""

# Django REST Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Models
from tasks.models import Task, Department, TaskStatus
from users.models import User

@api_view(["GET"])
def list_tasks(request):
    """List circles."""
    # import ipdb; ipdb.set_trace()

    tasks = Task.objects.all()

    data = []
    for task in tasks:
        data.append(
            {
                "user": task.user.username,  # Convertir a nombre de usuario
                "title": task.title,
                "description": task.description,
                "department": task.department.name,  # Convertir a nombre del departamento
                "status": task.status.name,  # Convertir a nombre del estado
                "hours": str(task.hours),  # Convertir a cadena de texto (HH:MM:SS)
            }
        )

    return Response(data)


@api_view(["POST"])
def create_task(request):
    """Create task"""
    user = User.objects.get(username=request.data["user"])
    title = request.data["title"]
    description = request.data["description"]
    department = Department.objects.get(pk=request.data["department"])
    status = TaskStatus.objects.get(pk=request.data["status"])
    hours = request.data["hours"]

    task = Task.objects.create(
        user=user,
        title=title,
        description=description,
        department=department,
        status=status,
        hours=hours,
    )

    data = {
        "user": task.user.username,  # Convertir a nombre de usuario
        "title": task.title,
        "description": task.description,
        "department": task.department.name,  # Convertir a nombre del departamento
        "status": task.status.name,  # Convertir a nombre del estado
        "hours": str(task.hours),  # Convertir a cadena de texto (HH:MM:SS)
    }
    return Response(data)
