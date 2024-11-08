"""Company model."""

# Django
from django.db import models

# Utilities
from flow.utils import FlowModels


class Company(FlowModels):
    """Model Company."""

    name = models.CharField(max_length=100, unique=True, verbose_name="nombre")

    def __str__(self) -> str:
        return str(self.name)
