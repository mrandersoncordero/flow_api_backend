"""Department Serializer."""

# Django REST Framework
from rest_framework import serializers

# Models
from petitions.models import Company


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
