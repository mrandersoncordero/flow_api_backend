"""Models tasks."""

# Django
from django.db import models

# Utilities
from flow.utils import FlowModels

class Task(FlowModels, models.Model):
    """Tasks model."""
