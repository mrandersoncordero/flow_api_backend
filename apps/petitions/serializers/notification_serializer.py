from rest_framework import serializers
from users.serializers.users import UserModelSerializer
from petitions.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer para el modelo de Notificaciones."""

    recipient = UserModelSerializer(
        read_only=True
    )
    
    class Meta:
        model = Notification
        fields = ["id", "recipient", "petition", "message", "status", "created_at"]
        read_only_fields = ["recipient", "created_at"]
