"""Petition views."""

# Django
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date

# Django REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    CreateAPIView,
    DestroyAPIView,
)
from rest_framework.views import APIView

# Models
from petitions.models import Petition
from users.models import User
from petitions.models import Company, Department

# Serializers
from petitions.serializers import (
    PetitionModelserializer,
    PetitionCreateSerializer,
    PetitionFullDetailserializer,
)

# DRF Yasg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Custom Permissions
from core.permissions import IsAdmin, IsManager, IsClient, IsEmployee, CanViewPetition
from core.functions import filter_queryset_by_group


class PetitionListView(ListAPIView):
    """Vista para listar peticiones con filtros avanzados."""

    queryset = Petition.active_objects.all()
    serializer_class = PetitionFullDetailserializer
    permission_classes = [IsAuthenticated, CanViewPetition]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="Token de autenticación. Usar el formato 'Token <ACCESS_TOKEN>'",
                type=openapi.TYPE_STRING,
                required=True,
                default="Token <ACCESS_TOKEN>",
            ),
            openapi.Parameter(
                "date_from",
                openapi.IN_QUERY,
                description="Filtrar peticiones desde esta fecha (YYYY-MM-DD).",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "date_until",
                openapi.IN_QUERY,
                description="Filtrar peticiones hasta esta fecha (YYYY-MM-DD).",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "title",
                openapi.IN_QUERY,
                description="Buscar peticiones por título.",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "user_id",
                openapi.IN_QUERY,
                description="Filtrar por usuario específico.",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "department_id",
                openapi.IN_QUERY,
                description="Filtrar por departamento específico.",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "company_id",
                openapi.IN_QUERY,
                description="Filtrar por empresa específica.",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={200: PetitionFullDetailserializer(many=True)},
    )
    def get_queryset(self):
        """Obtiene el queryset de peticiones aplicando filtros avanzados."""

        user = self.request.user  # Obtener usuario autenticado
        queryset = super().get_queryset()

        # Aplicar filtro de grupo antes de los filtros adicionales
        queryset = filter_queryset_by_group(queryset, user)

        # Filtros por query params
        date_from = self.request.query_params.get("date_from")
        date_until = self.request.query_params.get("date_until")
        title = self.request.query_params.get("title")
        user_id = self.request.query_params.get("user_id")
        department_id = self.request.query_params.get("department_id")
        company_id = self.request.query_params.get("company_id")

        if user_id:
            queryset = queryset.filter(user__id=user_id)

        if department_id:
            queryset = queryset.filter(department__id=department_id)

        if company_id:
            queryset = queryset.filter(company__id=company_id)

        if title:
            queryset = queryset.filter(title__icontains=title)

        if date_from:
            parsed_date = parse_date(date_from)
            if parsed_date:
                queryset = queryset.filter(created__gte=parsed_date)

        if date_until:
            parsed_date = parse_date(date_until)
            if parsed_date:
                queryset = queryset.filter(created__lte=parsed_date)

        return queryset


class PetitionDetailView(RetrieveAPIView):

    queryset = Petition.active_objects.all()
    serializer_class = PetitionFullDetailserializer
    permission_classes = [IsAuthenticated, CanViewPetition]

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
        responses={200: PetitionFullDetailserializer()},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PetitionUpdateView(UpdateAPIView):
    queryset = Petition.active_objects.all()
    serializer_class = PetitionModelserializer
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
        request_body=PetitionModelserializer,
        responses={
            200: openapi.Response("Peticion actualizada", PetitionModelserializer)
        },
    )
    def put(self, request, *args, **kwargs):
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
        request_body=PetitionModelserializer,
        responses={
            200: openapi.Response(
                "Peticion parcialmente actualizada", PetitionModelserializer
            )
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class PetitionDeleteView(DestroyAPIView):

    queryset = Petition.active_objects.all()
    serializer_class = PetitionModelserializer
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
        responses={
            200: openapi.Response(
                "Peticion eliminada",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Peticion eliminada correctamente",
                        )
                    },
                ),
            )
        },
    )
    def delete(self, request, *args, **kwargs):
        petition = self.get_object()
        petition.soft_delete()

        return Response(
            {"message": "Petición eliminada correctamente"},
            status=status.HTTP_200_OK,
        )


class PetitionCreateView(CreateAPIView):
    queryset = Petition.active_objects.all()
    serializer_class = PetitionCreateSerializer
    permission_classes = [IsAuthenticated, CanViewPetition]

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
            201: openapi.Response(
                "Petición creada",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Petición creada correctamente",
                        ),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "title": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    },
                ),
            )
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        petition = serializer.save()  # Guarda la petición

        return Response(
            {"message": "Petición creada correctamente", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class PetitionActivateView(APIView):
    """Activa una petición previamente eliminada (Soft Delete)."""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Activa una petición eliminada (Soft Delete).",
        responses={
            200: openapi.Response(
                description="Petición activada correctamente.",
                examples={
                    "application/json": {"message": "Petición activada correctamente."}
                },
            ),
            404: openapi.Response(
                description="Petición no encontrada.",
                examples={
                    "application/json": {
                        "error": "La petición no existe o ya está activa."
                    }
                },
            ),
        },
    )
    def patch(self, request, petition_id):
        """Activa una petición eliminada."""
        try:
            petition = Petition.active_objects.deleted().get(id=petition_id)
            petition.restore()
            return Response(
                {"message": "Petición activada correctamente."},
                status=status.HTTP_200_OK,
            )
        except Petition.DoesNotExist:
            return Response(
                {"error": "La petición no existe o ya está activa."},
                status=status.HTTP_404_NOT_FOUND,
            )
