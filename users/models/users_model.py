"""User model."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Utilities
from flow.utils import FlowModels


class User(FlowModels, AbstractUser):
    """User model.

    Extend form Django's Abstract User, change the username field
    to email and add some extra fields.
    """

    email = models.EmailField(
        "email address",
        unique=True,
        error_messages={"unique": "A user with that email already exists."},
    )

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    is_verified = models.BooleanField(
        "verified",
        default=False,
        help_text="Set to true when the user have verified its email address. ",
    )
    last_login = models.DateTimeField(
        verbose_name="Último inicio de sesión", default=timezone.now
    )

    def __str__(self):
        """Return username"""
        return str(self.username)

    def get_username(self) -> str:
        """Return username."""
        return self.username
