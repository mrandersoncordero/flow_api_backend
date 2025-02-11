"""Petitions serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from .models import Petition
from users.models import User

# Serializers
from users.serializers import UserModelSerializer

class PetitionModelserializer(serializers.ModelSerializer):
    """Petiion model serializer."""

    user = UserModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = Petition
        fields = [
            "id",
            "title",
            "description",
            "parent_petition",
            "priority",
            "status_approval",
            "department",
            "user",
            "active",
            "created",
            "modified",
            "deleted",
        ]