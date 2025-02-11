from rest_framework import serializers
from users.models import HumanResource, User
from users.serializers import UserModelSerializer  # Importamos el serializer de User


class HumanResourceModelSerializer(serializers.ModelSerializer):
    """Serializer para el modelo de HumanResource."""

    class Meta:
        model = HumanResource
        fields = ["biography", "phone_number", "picture"]

    def update(self, instance, validated_data):
        """Evitar que se intente modificar el usuario."""
        validated_data.pop(
            "user", None
        )  # Ignorar cualquier intento de modificar "user"
        return super().update(instance, validated_data)


class HumanResourceCreateSerializer(serializers.ModelSerializer):
    """Serializer para la creación de un HumanResource."""

    email = serializers.EmailField(write_only=True)  # Capturar email en la creacion

    class Meta:
        model = HumanResource
        fields = ["email", "biography", "phone_number", "picture"]

    def validate_email(self, value):
        """Verificar que el usuario existe antes de crear HumanResource."""
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No existe un usuario con este email.")

        if hasattr(user, "humanresource"):
            raise serializers.ValidationError(
                "Este usuario ya tiene un perfil HumanResource."
            )

        self.context["user"] = user
        return value

    def create(self, validated_data):
        """Crear un HumanResource asociado al usuario."""
        user = self.context["user"]
        validated_data.pop("email")
        return HumanResource.objects.create(user=user, **validated_data)
