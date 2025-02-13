"""Commissions Serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from .models import Commission
from petitions.models import Petition
from users.models import User


class CommissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Commission
        fields = "__all__"


class CommissionModelSerializer(serializers.ModelSerializer):

    petition_title = serializers.CharField(
        source="petition.title", read_only=True
    )  # Muestra el título de la petición asociada
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        """Meta class."""

        model = Commission
        fields = ["id", "description", "status", "users", "petition", "petition_title"]

        def validate_petition(self, value):
            """Valida que la peticion tenga is_main=False (solo peticiones secundarias)."""
            if value.is_main:
                raise serializers.ValidationError(
                    "Solo puedes asignar comisiones a peticiones secundarias (is_main=False)."
                )
            return value
