"""Petitions Model."""

# Django
from django.db import models

# Utilities
from flow.utils.main_model import MainModel

# Models
from .department_model import Department
from commissions.models import Commission
from users.models.human_resources_model import HumanResource


class Petition(MainModel, models.Model):
    """Petitions model.

    Args:
        MainModel (_type_): _description_
        models (_type_): _description_
    """

    class Priority(models.TextChoices):
        LOW = "LW", "LOW"
        MEDIUM = "MD", "MEDIUM"
        HIGH = "HG", "HIGH"
        URGENT = "UG", "URGENT"
        SUPER_URGENT = "SU", "SUPER_URGENT"
        STANDART = "ST", "STANDART"

    class StatusApproval(models.TextChoices):
        WAITING = "WT", "WAITING"
        APPROVED = "AP", "APPROVED"
        NOT_APPROVED = "NP", "NOT_APPROVED"

    parent_petition = models.ForeignKey(
        "self",  # Relación consigo mismo
        on_delete=models.SET_NULL,
        null=True,  # Permitir que sea nulo si no tiene padre
        blank=True,  # Hacerlo opcional
        related_name="child_petitions",  # Relación inversa para acceder a peticiones hijas
        verbose_name="parent petition",
    )
    title = models.CharField(verbose_name="title", max_length=120)
    description = models.TextField(verbose_name="description")
    priority = models.CharField(max_length=2, choices=Priority, default=Priority.LOW)
    status_approval = models.CharField(
        max_length=2, choices=StatusApproval, default=StatusApproval.WAITING
    )

    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="committees_on_petitions",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="departments",
    )
    human_resource = models.ForeignKey(HumanResource, on_delete=models.PROTECT)

    def clean(self):
        """Validaciones personalizadas para Petitions."""
        from django.core.exceptions import ValidationError

        # Si es una petición principal, no puede tener comisión
        if self.parent_petition is None and self.commission is not None:
            raise ValidationError(
                "Una petición principal no puede tener una comisión asignada."
            )

        # Si es una petición hija, debe tener una petición principal y una comisión
        if self.parent_petition is not None and self.commission is None:
            raise ValidationError(
                "Las peticiones hijas deben estar asociadas a una comisión."
            )

    def __str__(self):
        return f"{self.title} by {self.human_resource}"
    
    class Meta:
        db_table = 'petitions'