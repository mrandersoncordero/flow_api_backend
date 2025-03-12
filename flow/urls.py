"""URL configuration for flow project."""

# Django
from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.contrib import admin

# DRF Yasg
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Flow API",
        default_version="v1",  # 🔥 Cambiamos para usar versionamiento
        description="API para la gestión de usuarios, peticiones y comisiones.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@flowapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

urlpatterns = [
    # Documentación Swagger con versión en la URL
    path(
        "api/v1/swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "api/v1/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/v1/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    # Django Admin
    path("admin/", admin.site.urls),
    # 🔥 Agregamos prefijo `/api/v1/` para todas las apps
    path("api/v1/", include("users.urls", namespace="users")),
    path("api/v1/", include("petitions.urls", namespace="petitions")),
    path("api/v1/", include("commissions.urls", namespace="commissions")),
]
