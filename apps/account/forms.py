"""Forms for the account app."""
from django import forms
from django.contrib.auth.forms import AuthenticationForm

# Formulario pesonalizado para el inicio de sesión from django.contrib.auth
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))