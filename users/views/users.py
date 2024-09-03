"""Users views."""

# Django REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Models

# Serializers
from users.serializers import (
    UserLoginSerializer, 
    UserModelSerializer,
    UserSingUpSerializer
)

class UserLoginAPIView(APIView):
    """User login API view"""
    
    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        print(user)
        return Response(data, status=status.HTTP_201_CREATED)

class UserSingUpAPIView(APIView):
    """User Sing up API view."""

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = UserSingUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(data).data
        return Response(data, status=status.HTTP_201_CREATED)
