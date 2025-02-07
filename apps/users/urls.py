"""Users URLs."""

# Django
from django.urls import path

# Views
from .views import UserLoginAPIView, UserSingUpAPIView, AccountVerificationAPIView, UserAPIView

app_name = "users"

urlpatterns = [
    path("users/login/", UserLoginAPIView.as_view(), name="login"),
    path("users/singup/", UserSingUpAPIView.as_view(), name="signup"),
    path("users/verify/", AccountVerificationAPIView.as_view(), name="verify"),
    
    path('users/', UserAPIView.as_view(), name='list'),
    path('users/<int:pk>', UserAPIView.as_view()),
]
