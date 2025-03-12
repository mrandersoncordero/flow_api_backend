"""Model Department."""

# Django
from django.db import models

# Utilities
from flow.utils import FlowModels


class Department(FlowModels, models.Model):
    """Model Deparment."""

    name = models.CharField(max_length=120, 
                            unique=True, 
                            verbose_name="nombre")
    description = models.TextField(max_length=255, 
                                   blank=True, 
                                   null=True, 
                                   verbose_name='descripcion')
    
    def __str__(self) -> str:
        return f"{self.name}"