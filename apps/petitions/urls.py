from django.urls import path

from .views import PetitionListView

app_name = "petitions"

urlpatterns = [
    path("petitions/", PetitionListView.as_view(), name="petition-list"),
]
