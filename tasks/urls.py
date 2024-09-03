"""Taks URLs."""

# Django
from django.urls import path

# Views
from .views import list_tasks, create_task

app_name = 'tasks'

urlpatterns = [
    path('tasks/', list_tasks),
    path('tasks/create/', create_task),
]
