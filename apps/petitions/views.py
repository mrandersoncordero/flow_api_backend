"""Petition views."""

# Django
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date

# Dajngo REST Framework
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
from .models import Petition

# Serializers
from .serializers import PetitionModelserializer

# DRF Yasg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class PetitionListView(ListAPIView):
    queryset = Petition.objects.all()
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
        responses={200: PetitionModelserializer(many=True)},
    )
    def get_queryset(self):
        queryset = super().get_queryset()
        date_from = self.request.query_params.get("date_from", None)
        date_until = self.request.query_params.get("date_until", None)
        title = self.request.query_params.get("title", None)

        if title:
            queryset = queryset.filter(title__icontains=title)

        if date_from:
            date_from = parse_date(date_from)
            if date_from:
                queryset = queryset.filter(created__gte=date_from)

        if date_until:
            date_until = parse_date(date_until)
            if date_until:
                queryset = queryset.filter(created__lte=date_until)
