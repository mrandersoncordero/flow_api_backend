"""Department model."""

# Django
from django.db import models

# Utilities
from flow.utils.main_model import MainModel

class Department(MainModel, models.Model):
    """Department

    Args:
        MainModel (_type_): _description_
        models (_type_): _description_
    """

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'departments'