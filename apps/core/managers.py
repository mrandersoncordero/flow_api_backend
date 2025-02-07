# Django
from django.db import models
from django.utils.timezone import now

class ActiveManager(models.Manager):
    """Manager que solo devuelve registros activos."""

    def get_queryset(self):
        return super().get_queryset().filter(active=True, deleted__isnull=True)

    def deleted(self):
        """Devuelve los registros eliminados (soft-delete)."""
        return super().get_queryset().filter(active=False, deleted__isnull=False)

    def all_with_deleted(self):
        """Devuelve todos los registros, incluyendo eliminados."""
        return super().get_queryset()