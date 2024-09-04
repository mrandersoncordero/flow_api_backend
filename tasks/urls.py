"""Taks URLs."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import list_tasks, create_task, DepartmentViewSet

app_name = 'tasks'

router = DefaultRouter()
router.register(r'', DepartmentViewSet, basename='department')

urlpatterns = [
    path('tasks/', list_tasks),
    path('tasks/create/', create_task),
    path('departments/', include(router.urls)),
]
