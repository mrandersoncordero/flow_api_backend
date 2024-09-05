"""Department serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from tasks.models import Department


class DeparmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'created', 'modified']
        read_only_fields = ['created', 'modified']