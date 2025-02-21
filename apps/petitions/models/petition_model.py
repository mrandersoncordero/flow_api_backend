"""Petitions Model."""

# Django
from django.db import models

# Utilities
from utils.main_model import MainModel

# Models
from .department_model import Department
from .company_model import Company
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
        DONE = "DN", "DONE"

    is_main = models.BooleanField(default=True, verbose_name="Is main petition")

    title = models.CharField(verbose_name="Title", max_length=120)
    description = models.TextField(verbose_name="Description")
    priority = models.CharField(max_length=2, choices=Priority, default=Priority.LOW)
    status_approval = models.CharField(
        max_length=2, choices=StatusApproval, default=StatusApproval.WAITING
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="departments",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="companies",
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    hours = models.DurationField(verbose_name="tiempo invertido", null=True, blank=True)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} by {self.user}"

    class Meta:
        db_table = "petitions"
