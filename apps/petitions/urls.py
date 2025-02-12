from django.urls import path

from .views import (
    PetitionListView,
    PetitionDetailView,
    PetitionUpdateView,
    PetitionDeleteView,
    PetitionCreateView,
)

app_name = "petitions"

urlpatterns = [
    path("petitions/", PetitionListView.as_view(), name="petition-list"),
    path("petitions/<int:pk>/", PetitionDetailView.as_view(), name="petition-detail"),
    path(
        "petitions/create/",
        PetitionCreateView.as_view(),
        name="petition-create",
    ),
    path(
        "petitions/<int:pk>/update/",
        PetitionUpdateView.as_view(),
        name="petition-update",
    ),
    path(
        "petitions/<int:pk>/delete/",
        PetitionDeleteView.as_view(),
        name="petition-delete",
    ),
]
