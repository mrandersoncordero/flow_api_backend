from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()

class AuditLog(models.Model):
    """Modelo para registrar auditorías en el sistema."""

    ACTIONS = [
        ("CREATE", "Creación"),
        ("UPDATE", "Actualización"),
        ("DELETE", "Eliminación"),
        ("RESTORE", "Restauración"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    model_name = models.CharField(max_length=255)  # Nombre del modelo afectado
    object_id = models.PositiveIntegerField()  # ID del objeto afectado
    action = models.CharField(max_length=10, choices=ACTIONS)
    timestamp = models.DateTimeField(auto_now_add=True)  # Hora de la acción
    changes = models.JSONField(null=True, blank=True)  # Guardar cambios como JSON

    class Meta:
        db_table = "audit_logs"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.get_action_display()} - {self.model_name} ({self.object_id}) por {self.user}"