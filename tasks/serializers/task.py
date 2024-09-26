"""Task serializers."""

# Django REST Framework
from django.forms import ValidationError
from rest_framework import serializers

# Models
from tasks.models import Task, Department, TaskStatus, Company
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ["name"]


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ["name"]


class TaskStatusSerializer(serializers.ModelSerializer):
    """Tasks status model serializer."""

    class Meta:
        """Meta class."""

        model = TaskStatus
        fields = ["name"]


class TaskStatusModelSerializer(serializers.ModelSerializer):
    """Tasks status model serializer."""

    class Meta:
        """Meta class."""

        model = TaskStatus
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user_data = serializers.SerializerMethodField()
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    department_data = serializers.SerializerMethodField()
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    company_data = serializers.SerializerMethodField()
    status = serializers.PrimaryKeyRelatedField(queryset=TaskStatus.objects.all())
    status_data = serializers.SerializerMethodField()

    hours_display = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "user",  # Recibe y representa como ID en solicitudes
            "user_data",  # Representa el username en la respuesta
            "title",
            "description",
            "department",
            "department_data",
            "company",
            "company_data",
            "status",
            "status_data",
            "hours",  # Duración en el formato timedelta original
            "hours_display",  # Duración formateada como HH:MM
            "created",
            "start_date",
            "end_date",
            "modified",
        ]
        read_only_fields = ["created", "modified"]

    def get_user_data(self, obj):
        user_serializer = UserSerializer(obj.user)
        return user_serializer.data if obj.user else None

    def get_department_data(self, obj):
        department = (
            obj.department
        )  # Asegúrate de que estás accediendo al campo correcto
        department_serializer = DepartmentSerializer(department)
        return department_serializer.data if department else None

    def get_company_data(self, obj):
        company = obj.company  # Asegúrate de que estás accediendo al campo correcto
        company_serializer = CompanySerializer(company)
        return company_serializer.data if company else None

    def get_status_data(self, obj):
        status = obj.status  # Asegúrate de que estás accediendo al campo correcto
        status_serializer = TaskStatusSerializer(status)
        return status_serializer.data if status else None

    def get_hours_display(self, obj):
        if obj.hours:
            total_seconds = int(obj.hours.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours} horas {minutes} minutos"
        return None

    def clean(self):
        if isinstance(self.hours, str):
            raise ValidationError("El campo hours no puede ser una cadena de texto.")
