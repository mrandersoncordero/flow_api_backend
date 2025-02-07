"""Document model."""

# Django
from django.db import models

# Utilities
from utils.main_model import MainModel

# Models
from .commission_model import Commission

class Document(MainModel, models.Model):
    """Document

    Args:
        MainModel (_type_): _description_
        models (_type_): _description_
    """

    path = models.CharField(max_length=255)
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE, related_name='comissions')

    def __str__(self):
        return f"{self.commission.description}"
    
    class Meta:
        db_table = "documents"
        indexes = [
            models.Index(fields=['id', 'active']),
        ]