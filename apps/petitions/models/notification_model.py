from django.db import models
from django.contrib.auth import get_user_model
from petitions.models import Petition

User = get_user_model()

class Notification(models.Model):
    """Modelo para gestionar notificaciones."""

    class Status(models.TextChoices):
        UNREAD = "unread", "No Leída"
        READ = "read", "Leída"

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    petition = models.ForeignKey(
        Petition, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.TextField()
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.UNREAD
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificación para {self.recipient.email}: {self.message}"