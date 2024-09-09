"""Views Company."""

# Django
from django.db.models import ProtectedError

# Django REST Framework
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Models
from tasks.models import Company

# Serializers
from tasks.serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        company = self.get_object()
        try:
            self.perform_destroy(company)
        except ProtectedError:
            return Response(
                {"detail": "Cannot delete this company as it has associated tasks."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_204_NO_CONTENT)