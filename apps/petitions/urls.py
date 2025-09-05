from django.urls import path

from .views import (
    # Petitions views
    PetitionListView,
)

app_name = "petitions"

urlpatterns = [
    # Petitions
    path("petitions/", PetitionListView.as_view(), name="list"),]