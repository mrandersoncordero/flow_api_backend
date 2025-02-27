"""Users views."""

# Django
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group

# Django REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

# Models
from users.models import User

# Serializers
from users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSingUpSerializer,
    AccountVerificationSerializer,
)

# DRF Yasg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Custom Permissions
from core.permissions import IsAdmin, IsManager, IsClient, IsEmployee
from core.functions import filter_queryset_user_by_group


class UserLoginAPIView(APIView):
    """User login API view"""

    @swagger_auto_schema(
        request_body=UserLoginSerializer,  # Especificamos el esquema de entrada
        responses={
            201: openapi.Response("Login exitoso", UserModelSerializer)
        },  # Respuesta esperada
    )
    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {"user": UserModelSerializer(user).data, "access_token": token}
        print(user)
        return Response(data, status=status.HTTP_201_CREATED)


class UserSingUpAPIView(APIView):
    """User Sing up API view."""

    @swagger_auto_schema(
        request_body=UserSingUpSerializer,
        responses={201: openapi.Response("Registro exitoso", UserModelSerializer)},
    )
    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = UserSingUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)


class AccountVerificationAPIView(APIView):
    """Account verification API view."""

    @swagger_auto_schema(
        request_body=AccountVerificationSerializer,
        responses={
            200: openapi.Response(
                "Cuenta verificada",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING, example="Congratulations!"
                        )
                    },
                ),
            )
        },
    )
    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"message": "Congratulation!"}
        return Response(data, status=status.HTTP_200_OK)


### 🔹 1. GET ALL (Lista de usuarios) ###
class UserListView(ListAPIView):
    """Lista todos los usuarios con filtros opcionales."""

    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsClient | IsManager | IsEmployee]

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
            openapi.Parameter(
                "email",
                openapi.IN_QUERY,
                description="Filtrar por email",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "active",
                openapi.IN_QUERY,
                description="Filtrar por estado activo",
                type=openapi.TYPE_BOOLEAN,
            ),
            openapi.Parameter(
                "verified",
                openapi.IN_QUERY,
                description="Filtrar por estado verificado",
                type=openapi.TYPE_BOOLEAN,
            ),
        ],
        responses={200: UserModelSerializer(many=True)},
    )
    def get_queryset(self):
        """Filtrar usuarios por email, estado activo y verificado."""
        user = self.request.user  # Obtener usuario autenticado
        queryset = super().get_queryset()
        
        email = self.request.query_params.get("email")
        active = self.request.query_params.get("active")
        verified = self.request.query_params.get("verified")
        group = self.request.query_params.get("group")
        exclude_group_name = self.request.query_params.get("exclude_group")

        if email:
            queryset = queryset.filter(email__icontains=email)
        if active is not None:
            queryset = queryset.filter(is_active=active.lower() == "true")
        if verified is not None:
            queryset = queryset.filter(is_verified=verified.lower() == "true")
        # Filtrar por grupo
        if group:
            queryset = queryset.filter(groups__name=group)
        # Excluir usuarios de un grupo
        if exclude_group_name:
            queryset = queryset.exclude(groups__name=exclude_group_name)
        
        return queryset.distinct()


### 🔹 2. GET by ID (Detalle de usuario) ###
class UserDetailView(RetrieveAPIView):
    """Obtiene un usuario por ID."""

    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

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
        responses={200: UserModelSerializer()},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


### 🔹 3. PUT / PATCH (Actualizar usuario) ###
class UserUpdateView(UpdateAPIView):
    """Actualiza un usuario completamente (PUT) o parcialmente (PATCH)."""

    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

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
        request_body=UserModelSerializer,
        responses={200: openapi.Response("Usuario actualizado", UserModelSerializer)},
    )
    def put(self, request, *args, **kwargs):
        """PUT - Actualiza todos los campos."""
        return super().put(request, *args, **kwargs)

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
        request_body=UserModelSerializer,
        responses={
            200: openapi.Response(
                "Usuario parcialmente actualizado", UserModelSerializer
            )
        },
    )
    def patch(self, request, *args, **kwargs):
        """PATCH - Actualiza solo algunos campos."""
        return super().patch(request, *args, **kwargs)


### 🔹 4. DELETE (Eliminar usuario) ###
class UserDeleteView(DestroyAPIView, IsAdmin):
    """Elimina un usuario."""

    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated]

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
        responses={
            200: openapi.Response(
                "Usuario eliminado",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Usuario eliminado correctamente",
                        )
                    },
                ),
            )
        },
    )
    def delete(self, request, *args, **kwargs):
        """DELETE - Elimina un usuario por ID."""
        response = super().delete(request, *args, **kwargs)
        return Response(
            {"message": "Usuario eliminado correctamente"}, status=status.HTTP_200_OK
        )


class UserAPIView(APIView):
    """Retrieve a user or list users"""

    permission_classes = [IsAuthenticated, IsAdmin]

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
            openapi.Parameter(
                "email",
                openapi.IN_QUERY,
                description="Filtrar por email",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "active",
                openapi.IN_QUERY,
                description="Filtrar por estado activo",
                type=openapi.TYPE_BOOLEAN,
            ),
            openapi.Parameter(
                "verified",
                openapi.IN_QUERY,
                description="Filtrar por estado verificado",
                type=openapi.TYPE_BOOLEAN,
            ),
        ],
        responses={200: UserModelSerializer(many=True)},
    )
    def get(self, request, pk=None):
        if pk:
            user = get_object_or_404(User, pk=pk)
            serializer = UserModelSerializer(user)
            return Response(serializer.data)

        queryset = User.objects.all()
        email = request.query_params.get("email", None)
        active = request.query_params.get("active", None)
        verified = request.query_params.get("verified", None)

        try:
            if email:
                queryset = queryset.filter(email__icontains=email)
            if active:
                queryset = queryset.filter(is_active=active)
            if verified:
                queryset = queryset.filter(is_verified=verified)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Ocurrió un error inesperado."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        serializer = UserModelSerializer(queryset, many=True)
        return Response(serializer.data)


class AddUserToGroupView(APIView):
    """Agrega un usuario a un grupo."""

    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description="Agrega un usuario a un grupo específico.",
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
        responses={
            200: openapi.Response(
                "Usuario agregado correctamente",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Usuario juan@example.com agregado al grupo Admin.",
                        )
                    },
                ),
            ),
            404: openapi.Response(
                "Usuario no encontrado",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="No se encontró el usuario o el grupo.",
                        )
                    },
                ),
            ),
        },
    )
    def post(self, request, user_id, group_name):
        """Asigna un usuario a un grupo."""
        user = get_object_or_404(User, id=user_id)
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

        return Response(
            {"message": f"Usuario {user.email} agregado al grupo {group_name}."},
            status=status.HTTP_200_OK,
        )


class RemoveUserFromGroupView(APIView):
    """Elimina un usuario de un grupo."""

    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description="Elimina un usuario de un grupo específico.",
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
        responses={
            200: openapi.Response(
                "Usuario eliminado correctamente",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Usuario juan@example.com eliminado del grupo Admin.",
                        )
                    },
                ),
            ),
            400: openapi.Response(
                "Error: El usuario no pertenece al grupo",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="El usuario juan@example.com no está en el grupo Admin.",
                        )
                    },
                ),
            ),
            404: openapi.Response(
                "Usuario o grupo no encontrado",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="No se encontró el usuario o el grupo.",
                        )
                    },
                ),
            ),
        },
    )
    def delete(self, request, user_id, group_name):
        """Elimina un usuario de un grupo."""
        user = get_object_or_404(User, id=user_id)
        group = get_object_or_404(Group, name=group_name)

        if group in user.groups.all():
            user.groups.remove(group)
            return Response(
                {"message": f"Usuario {user.email} eliminado del grupo {group_name}."},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": f"El usuario {user.email} no está en el grupo {group_name}."},
            status=status.HTTP_400_BAD_REQUEST,
        )
