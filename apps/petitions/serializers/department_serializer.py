"""Department Serializer."""

# Django REST Framework
from rest_framework import serializers

# Models
from petitions.models import Department


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
