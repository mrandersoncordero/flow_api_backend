"""Utils models."""

# Django
from django.db import models

class FlowModels(models.Model):
    """Flow base model.
      + created (DateTime): Store the datetime the objects was created.
      + modified (DateTime): Store the datetime the objects was modified
    """

    created = models.DateTimeField(
        'created',
        auto_now_add=True,
        help_text='Date time on which the object was created'
    )

    modified = models.DateTimeField(
        'modified',
        auto_now=True,
        help_text='Date time on which the object was last modified'
    )

    class Meta:
        """Meta options."""
        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-modified']