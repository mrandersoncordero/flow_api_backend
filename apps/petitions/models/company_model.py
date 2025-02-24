"""Company model."""

# Django
from django.db import models

# Utilities
from utils.main_model import MainModel


class Company(MainModel, models.Model):
    """Model Company."""

    name = models.CharField(max_length=100, unique=True, verbose_name="nombre")

    class Meta:
        indexes = [
            models.Index(fields=['active', 'deleted'])
        ]

    def __str__(self) -> str:
        return str(self.name)