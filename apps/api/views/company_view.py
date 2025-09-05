"""Department views."""

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

# Models
from petitions.models import Company, Petition
from users.models import HumanResource

# Serializers
from petitions.serializers import CompanySerializer, CompanyCreateSerializer

# DRF Yasg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Custom Permissions
from core.permissions import IsAdmin, IsManager, IsEmployee, IsClient


class CompanyListView(ListAPIView):
    queryset = Company.active_objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsManager | IsEmployee | IsClient]

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
        responses={200: CompanySerializer(many=True)},
    )
    def get_queryset(self):
        return super().get_queryset()


class CompanyDetailView(RetrieveAPIView):
    queryset = Company.active_objects.all()
    serializer_class = CompanySerializer
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
        responses={200: CompanySerializer()},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CompanyUpdateView(UpdateAPIView):
    queryset = Company.active_objects.all()
    serializer_class = CompanySerializer
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
        request_body=CompanySerializer,
        responses={
            200: openapi.Response("Empresa actualizada", CompanySerializer)
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
        request_body=CompanySerializer,
        responses={
            200: openapi.Response(
                "Empresa parcialmente actualizada", CompanySerializer
            )
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class CompanyDeleteView(DestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
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
                "Empresa eliminada",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Empresa eliminada correctamente",
                        )
                    },
                ),
            )
        },
    )
    def delete(self, request, *args, **kwargs):
        company = self.get_object()
        # 🔥 Verificar si hay peticiones activas asociadas a esta empresa
        if Petition.active_objects.filter(company=company).exists():
            return Response(
                {
                    "error": "No se puede eliminar la empresa porque tiene peticiones activas."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # 🔥 Verificar si hay recursos humanos activos asociados a esta empresa
        if HumanResource.active_objects.filter(company=company).exists():
            return Response(
                {
                    "error": "No se puede eliminar la empresa porque tiene usuarios activos."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        company.soft_delete()
        return Response(
            {"message": "Empresa eliminada correctamente"},
            status=status.HTTP_200_OK,
        )


class CompanyCreateView(CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyCreateSerializer
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
            201: openapi.Response(
                "Empresa creada",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Empresa creada correctamente",
                        ),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "name": openapi.Schema(type=openapi.TYPE_STRING),
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
        serializer.save()

        return Response(
            {"message": "Empresa creada correctamente", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )