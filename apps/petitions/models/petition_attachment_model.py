"""Petitions Attachment model."""

# Django
from django.db import models

# Utilities
from utils.main_model import MainModel

# Models
from petitions.models.petition_model import Petition

class PetitionsAttachment(MainModel, models.Model):
    """PetitionsAttachment

    Args:
        MainModel (_type_): _description_
        models (_type_): _description_
    """

    path = models.CharField(max_length=255)
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='requests')

    def __str__(self):
        return f"{self.request.petition.title}"
    
    class Meta:
        db_table = 'petition_attachment'