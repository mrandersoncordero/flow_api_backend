"""Users views."""

# Django
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

# Django REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Models
from users.models import User

# Serializers
from users.serializers import (
    UserLoginSerializer, 
    UserModelSerializer,
    UserSingUpSerializer,
    AccountVerificationSerializer
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
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

class AccountVerificationAPIView(APIView):
    """Account verification API view."""

    def post(self, request, *args, **kwargs):
        """Handlre HTTP POST request."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulation!'}
        return Response(data, status=status.HTTP_200_OK)
    

class UserAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        
        if pk:
            user = get_object_or_404(User, pk=pk)
            serializer = UserModelSerializer(user)
            return Response(serializer.data)

        queryset = User.objects.all()
        email = request.query_params.get('email', None)
        active = request.query_params.get('active', None)
        verified = request.query_params.get('verified', None)

        try:
            if email:
                queryset = queryset.filter(email__icontains=email)
            if active:
                queryset = queryset.filter(is_active=active)
            if verified:
                queryset = queryset.filter(is_verified=verified)

        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Ocurrió un error inesperado."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        serializer = UserModelSerializer(queryset, many=True)
        return Response(serializer.data)
