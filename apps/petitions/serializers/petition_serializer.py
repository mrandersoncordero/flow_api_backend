"""Petitions serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from petitions.models import Petition, Department, Company
from users.models import User

# Serializers
from users.serializers import UserModelSerializer, ClientCompanySerializer
from commissions.serializers import CommissionSerializer
from .department_serializer import DepartmentSerializer
from .company_serializer import CompanySerializer

from datetime import timedelta


class PetitionFullDetailserializer(serializers.ModelSerializer):
    """Petiion model serializer."""

    user = UserModelSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    client_companies = ClientCompanySerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    commissions = CommissionSerializer(many=True, read_only=True)

    class Meta:
        """Meta class."""

        model = Petition
        fields = [
            "id",
            "title",
            "description",
            "is_main",
            "priority",
            "status_approval",
            "department",
            "company",
            "user",
            "commissions",
            "active",
            "hours",
            "client_companies",
            "start_date",
            "end_date",
            "created",
            "modified",
            "deleted",
        ]

    def validate(self, data):
        """Valida que `end_date` sea mayor que `start_date`."""
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date and end_date:  # Solo validar si ambas fechas están presentes
            if end_date <= start_date:
                raise serializers.ValidationError(
                    {
                        "end_date": "La fecha de finalización debe ser posterior a la fecha de inicio."
                    }
                )
        return data


class PetitionModelserializer(serializers.ModelSerializer):
    """Petiion model serializer."""

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    hours = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        """Meta class."""

        model = Petition
        fields = [
            "id",
            "title",
            "description",
            "is_main",
            "priority",
            "status_approval",
            "department",
            "company",
            "user",
            "active",
            "hours",
            "start_date",
            "end_date",
            "created",
            "modified",
            "deleted",
        ]

    def validate_hours(self, value):
        """Convierte `HH:MM` a `timedelta`."""
        if value:
            try:
                hours, minutes = map(int, value.split(":"))  # Separar HH y MM
                return timedelta(hours=hours, minutes=minutes)
            except ValueError:
                raise serializers.ValidationError(
                    "El formato de horas debe ser 'HH:MM'."
                )
        return None

    def validate(self, data):
        """Valida que `end_date` sea mayor que `start_date`."""
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date and end_date:  # Solo validar si ambas fechas están presentes
            if end_date <= start_date:
                raise serializers.ValidationError(
                    {
                        "end_date": "La fecha de finalización debe ser posterior a la fecha de inicio."
                    }
                )
        return data


class PetitionCreateSerializer(serializers.ModelSerializer):

    hours = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Petition
        fields = [
            "title",
            "description",
            "is_main",
            "priority",
            "status_approval",
            "department",
            "company",
            "user",
            "active",
            "hours",
            "start_date",
            "end_date",
        ]

    def validate(self, data):
        """Valida que `end_date` sea mayor que `start_date`."""
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date and end_date:  # Solo validar si ambas fechas están presentes
            if end_date <= start_date:
                raise serializers.ValidationError(
                    {
                        "end_date": "La fecha de finalización debe ser posterior a la fecha de inicio."
                    }
                )
        return data

    def validate_hours(self, value):
        """Convierte `HH:MM` a `timedelta`."""
        if value:
            try:
                hours, minutes = map(int, value.split(":"))  # Separar HH y MM
                return timedelta(hours=hours, minutes=minutes)
            except ValueError:
                raise serializers.ValidationError(
                    "El formato de horas debe ser 'HH:MM'."
                )
        return None
