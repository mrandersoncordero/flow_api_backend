"""Main model."""

# Django
from django.db import models
from django.db.models.functions import Now

# Models
from .base_model import BaseModel


class MainModel(BaseModel):
    """MainModel

    Args:
        BaseModel (_type_): _description_
    """

    deleted = models.DateTimeField(verbose_name="deleted", default=None)

    active = models.BooleanField(verbose_name="active", default=True, help_text="")

    def onDelete(self):
        self.deleted = Now()
        self.active = False

    def restore(self):
        self.deleted = None
        self.active = True

    class Meta:
        """Meta options."""
        abstract = True
