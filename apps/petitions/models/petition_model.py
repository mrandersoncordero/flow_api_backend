"""Petitions Model."""

# Django
from django.db import models

# Utilities
from utils.main_model import MainModel

# Models
from .department_model import Department
from commissions.models import Commission
from users.models.users_model import User


class Petition(MainModel, models.Model):
    """Modelo de Petición.

    Una petición puede tener varias comisiones asociadas.
    """

    class Priority(models.TextChoices):
        LOW = "LW", "LOW"
        MEDIUM = "MD", "MEDIUM"
        HIGH = "HG", "HIGH"
        URGENT = "UG", "URGENT"
        SUPER_URGENT = "SU", "SUPER_URGENT"
        STANDARD = "ST", "STANDARD"

    class StatusApproval(models.TextChoices):
        WAITING = "WT", "WAITING"
        APPROVED = "AP", "APPROVED"
        NOT_APPROVED = "NP", "NOT_APPROVED"

    parent_petition = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="child_petitions",
        verbose_name="parent petition",
    )
    title = models.CharField(verbose_name="title", max_length=120)
    description = models.TextField(verbose_name="description")
    priority = models.CharField(
        max_length=2, choices=Priority, default=Priority.LOW
    )
    status_approval = models.CharField(
        max_length=2, choices=StatusApproval, default=StatusApproval.WAITING
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="departments",
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def clean(self):
        """Validaciones personalizadas para Petitions."""
        from django.core.exceptions import ValidationError

        # Si es una petición principal, no puede tener comisiones
        if self.parent_petition is None and self.commissions.exists():
            raise ValidationError(
                "Una petición principal no puede tener comisiones asignadas."
            )

        # Si es una petición hija, debe tener una petición principal y al menos una comisión
        if self.parent_petition is not None and not self.commissions.exists():
            raise ValidationError(
                "Las peticiones hijas deben estar asociadas a al menos una comisión."
            )

    def __str__(self):
        return f"{self.title} by {self.user}"

    class Meta:
        db_table = "petitions"
