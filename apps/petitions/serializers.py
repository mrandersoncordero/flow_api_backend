"""Petitions serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from .models import Petition, Company, Department
from commissions.models import Commission
from users.models import User

# Serializers
from users.serializers import UserModelSerializer
from commissions.serializers import CommissionSerializer

class DepartmentSerializer(serializers.ModelSerializer):
    """Department serializer."""

    class Meta:
        model = Department
        fields = "__all__"


class DepartmentCreateSerializer(serializers.ModelSerializer):
    """Create Department Serializer."""

    class Meta:
        model = Department
        fields = ["name"]

class CompanySerializer(serializers.ModelSerializer):
    """Company serializer."""

    class Meta:
        model = Company
        fields = "__all__"


class CompanyCreateSerializer(serializers.ModelSerializer):
    """Create Company Serializer."""

    class Meta:
        model = Company
        fields = ["name"]

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
