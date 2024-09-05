"""Company Serializer."""

# Django REST Framework
from rest_framework import serializers

# Models
from tasks.models import Company

class CompanySerializer(serializers.ModelSerializer):
    """Company model serializer."""

    class Meta:
        """Meta class."""
        model = Company
        fields = ['id', 'name', 'created', 'modified']
        read_only_fields = ['created', 'modified']
