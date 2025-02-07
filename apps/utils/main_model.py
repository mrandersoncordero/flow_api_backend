"""Main model."""

# Django
from django.db import models
from django.utils.timezone import now

# Utilities
from .base_model import BaseModel
from apps.core.managers import ActiveManager  # Importamos el nuevo manager


class MainModel(BaseModel):
    """Modelo base para incluir `active` y `deleted`."""

    deleted = models.DateTimeField(
        verbose_name="deleted", default=None, null=True, blank=True
    )

    active = models.BooleanField(verbose_name="Activo", default=True, help_text="")

    objects = ActiveManager()  # 🔥 Filtra por defecto solo activos

    def soft_delete(self):
        """Elimina el objeto sin borrarlo de la BD (Soft Delete)."""
        self.deleted = now()
        self.active = False
        self.save()

    def restore(self):
        """Restaura un objeto eliminado."""
        self.deleted = None
        self.active = True
        self.save()

    class Meta:
        """Meta options."""

        abstract = True
