"""User model."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Now

# Utilities
from utils.main_model import MainModel

class User(MainModel, AbstractUser):
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
        verbose_name="Último inicio de sesión", default=Now()
    )

    def get_username(self) -> str:
        """Return username."""
        return self.username

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["active"]),
        ]
        db_table = 'users'

    def __str__(self):
        """Return username"""
        return str(self.username)