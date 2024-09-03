"""Users serializers."""

# Django
from django.contrib.auth import authenticate

# Django REST Frameork
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Models
from users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    """User model serilizer."""

    class Meta:
        """Meta class."""

        model = User
        fields = ("username", "first_name", "last_name", "email")


class UserLoginSerializer(serializers.Serializer):
    """User Login Serializer.

    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=4, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        self.context["user"] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""
        token, created = Token.objects.get_or_create(user=self.context["user"])
        return self.context["user"], token.key
