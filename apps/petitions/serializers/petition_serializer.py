"""Petitions serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from petitions.models import Petition

# Serializers
from users.serializers import UserModelSerializer
from commissions.serializers import CommissionSerializer
from .department_serializer import DepartmentSerializer
from .company_serializer import CompanySerializer


class PetitionFullDetailserializer(serializers.ModelSerializer):
    """Petiion model serializer."""

    user = UserModelSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
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
            "created",
            "modified",
            "deleted",
        ]


class PetitionModelserializer(serializers.ModelSerializer):
    """Petiion model serializer."""

    user = UserModelSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)

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
            "created",
            "modified",
            "deleted",
        ]


class PetitionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Petition
        fields = [
            "title",
            "description",
            "is_main",
            "priority",
            "status_approval",
            "department",
            "user",
            "active",
        ]
