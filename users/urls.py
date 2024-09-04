"""Users URLs."""

# Django
from django.urls import path

# Views
from .views import UserLoginAPIView, UserSingUpAPIView, AccountVerificationAPIView

app_name = "users"

urlpatterns = [
    path("users/login/", UserLoginAPIView.as_view(), name="login"),
    path("users/singup/", UserSingUpAPIView.as_view(), name="signup"),
    path("users/verify/", AccountVerificationAPIView.as_view(), name="verify"),
]
