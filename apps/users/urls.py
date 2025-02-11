"""Users URLs."""

# Django
from django.urls import path

# Views
from .views import (
    UserLoginAPIView,
    UserSingUpAPIView,
    AccountVerificationAPIView,
    UserListView,
    UserDetailView,
    UserUpdateView,
    UserDeleteView,
    HumanResourceCreateAPIView,
    HumanResourceDetailUpdateAPIView
)

app_name = "users"

urlpatterns = [
    path("users/login/", UserLoginAPIView.as_view(), name="login"),
    path("users/singup/", UserSingUpAPIView.as_view(), name="signup"),
    path("users/verify/", AccountVerificationAPIView.as_view(), name="verify"),
    path("users/", UserListView.as_view(), name="user-list"),  # GET All
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),  # GET by ID
    path("users/<int:pk>/update/", UserUpdateView.as_view(), name="user-update"),  # PUT / PATCH
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user-delete"),  # DELETE

    path(
        "human-resources/",
        HumanResourceCreateAPIView.as_view(),
        name="create-human-resource",
    ),
    path(
        "human-resources/me/",
        HumanResourceDetailUpdateAPIView.as_view(),
        name="detail-update-human-resource",
    ),
]
