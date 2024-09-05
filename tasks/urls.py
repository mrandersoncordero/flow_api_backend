"""Taks URLs."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import TaskViewSet, DepartmentViewSet, TaskStatusAPIView

app_name = 'tasks'

router_department = DefaultRouter()
router_department.register(r'', DepartmentViewSet, basename='department')

router_task = DefaultRouter()
router_task.register(r'', TaskViewSet, basename='tasks')

urlpatterns = [
    path('tasks/', include(router_task.urls)),

    path('status_tasks/', TaskStatusAPIView.as_view()),
    path('status_task/<int:pk>/', TaskStatusAPIView.as_view()),

    path('departments/', include(router_department.urls)),
]
