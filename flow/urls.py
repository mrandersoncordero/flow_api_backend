"""URL configuration for flow project."""

# Django
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),
    # API v1
    path("api/v1/", include("api.urls", namespace="api")),
]
