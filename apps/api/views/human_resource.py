"""API human_resource view."""

# Django Rest Framework
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView

# DRF Yasg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Models
from users.serializers.human_resourse import (
    HumanResourceModelSerializer,
    HumanResourceCreateSerializer,
)

# Custom Permissions
from core.permissions import IsAdmin

class HumanResourceCreateAPIView(CreateAPIView):
    """API para crear un perfil de HumanResource."""

    serializer_class = HumanResourceCreateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]  # Solo usuarios autenticados pueden crear HR

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="Token de autenticación. Usar el formato 'Token <access_token>'",
                type=openapi.TYPE_STRING,
                required=True,
                default="Token <ACCESS_TOKEN>",
            ),
        ],
        request_body=HumanResourceCreateSerializer,
        responses={201: HumanResourceModelSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class HumanResourceDetailUpdateAPIView(RetrieveUpdateAPIView):
    """API para obtener o actualizar el perfil de HumanResource del usuario autenticado."""

    serializer_class = HumanResourceModelSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self):
        """Retorna el perfil de HumanResource del usuario autenticado."""
        return self.request.user.humanresource

    @swagger_auto_schema(
        responses={200: HumanResourceModelSerializer},
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="Token de autenticación (Formato: 'Token <ACCESS_TOKEN>')",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=HumanResourceModelSerializer,
        responses={200: HumanResourceModelSerializer},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)