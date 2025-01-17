"""Base model."""

# Django
from django.db import models

# Utilities
import uuid


class BaseModel(models.Model):
    """Base Model.

    Args:
        id (UUID): primary key.
    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    created = models.DateTimeField(
        verbose_name="created",
        auto_now_add=True,
        help_text="Date time on which the object was created",
    )

    modified = models.DateTimeField(
        verbose_name="modified",
        auto_now=True,
        help_text="Date time on which the object was last modified",
    )

    class Meta:
        """Meta options."""
        abstract = True
        ordering = ["-created"]