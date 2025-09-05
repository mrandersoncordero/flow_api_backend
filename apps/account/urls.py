"""Account app URLs."""

from django.urls import path
from .forms import CustomLoginForm

from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    # Login and Logout
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="account/login.html",
            authentication_form=CustomLoginForm,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            next_page="account:login"
        ),
        name="logout",
    ),
]
