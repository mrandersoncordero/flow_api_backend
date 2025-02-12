"""Commision model."""

# Django
from django.db import models

# Utilities
from utils.main_model import MainModel
from users.models.users_model import User

from core.managers import ActiveManager

class Commission(MainModel, models.Model):
    """Modelo de Comisión.

    Una comisión pertenece a una única petición.
    """

    class CommissionStatus(models.TextChoices):
        OPEN = "OP", "OPEN"
        CLOSED = "CL", "CLOSED"

    description = models.CharField(max_length=255)
    status = models.CharField(
        max_length=2, choices=CommissionStatus, default=CommissionStatus.OPEN
    )
    users = models.ManyToManyField(User)

    # Relación: Una Comisión pertenece a UNA Petición
    petition = models.ForeignKey(
        "petitions.Petition",
        on_delete=models.CASCADE,
        related_name="commissions",
        limit_choices_to={"is_main": False},
    )

    def __str__(self):
        return f"{self.description} (Petition: {self.petition.title})"

    class Meta:
        db_table = "commissions"
        indexes = [
            models.Index(fields=["id", "active"]),
        ]
