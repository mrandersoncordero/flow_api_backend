"""Models tasks."""

# Django
from django.db import models
from django.conf import settings
from django.utils.timezone import datetime

# Utilities
from flow.utils import FlowModels

# Models
from tasks.models import Department, Company


class TaskStatus(models.Model):
    """TaskStatus model."""

    name = models.CharField(max_length=50, unique=True, verbose_name="nombre")

    def __str__(self) -> str:
        return f"{self.name}"


class Task(FlowModels, models.Model):
    """Tasks model."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=200, unique=True, verbose_name="titulo")
    description = models.TextField(
        max_length=500, null=True, blank=True, verbose_name="descripcion"
    )
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, default=1)
    status = models.ForeignKey(TaskStatus, on_delete=models.SET_NULL, null=True)
    hours = models.TimeField(verbose_name="tiempo")

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.title} - by {self.user.username}"
