"""Taks URLs."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import TaskViewSet, DepartmentViewSet, TaskStatusAPIView, CompanyViewSet

app_name = 'tasks'

router_department = DefaultRouter()
router_department.register(r'', DepartmentViewSet, basename='department')

router_task = DefaultRouter()
router_task.register(r'', TaskViewSet, basename='tasks')

router_company = DefaultRouter()
router_company.register(f'', CompanyViewSet, basename='company')

urlpatterns = [
    path('tasks/', include(router_task.urls)),

    path('status_tasks/', TaskStatusAPIView.as_view()),
    path('status_task/<int:pk>/', TaskStatusAPIView.as_view()),

    path('departments/', include(router_department.urls)),

    path('companies/', include(router_company.urls)),
]
