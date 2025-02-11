"""Human resources model."""

# Django
from django.db import models
from django.conf import settings

# Utilities
from utils.main_model import MainModel


class HumanResource(MainModel, models.Model):
    """HumanResource

    Args:
        MainModel (_type_): _description_
        models (_type_): _description_
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='human_resource'
    )
    biography = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    picture = models.ImageField(upload_to="users/pictures", blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["active"]),
        ]
        db_table = 'human_resources'
