"""Department views."""

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
from petitions.models import Company

# Serializers
from petitions.serializers import CompanySerializer, CompanyCreateSerializer

# DRF Yasg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CompanyListView(ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
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
        responses={200: CompanySerializer(many=True)},
    )
    def get_queryset(self):
        return super().get_queryset()


class CompanyDetailView(RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
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
        responses={200: CompanySerializer()},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CompanyUpdateView(UpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
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
        petition = self.get_object()
        petition.soft_delete()

        return Response(
            {"message": "Empresa eliminada correctamente"},
            status=status.HTTP_200_OK,
        )


class CompanyCreateView(CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyCreateSerializer
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
        petition = serializer.save()

        return Response(
            {"message": "Empresa creada correctamente", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )