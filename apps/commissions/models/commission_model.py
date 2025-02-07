"""Commision model."""

# Django
from django.db import models

# Utilities
from utils.main_model import MainModel
from users.models.users_model import User

class Commission(MainModel, models.Model):
    """Commission

    Args:
        MainModel (_type_): _description_
        models (_type_): _description_
    """

    class CommissionStatus(models.TextChoices):
        OPEN = 'OP', 'OPEN'
        CLOSED = 'CL', 'CLOSED'
    
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=2, choices=CommissionStatus, default=CommissionStatus.OPEN)
    users = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.description}"
    
    class Meta:
        db_table = "commisions"
        indexes = [
            models.Index(fields=['id', 'active']),
        ]
