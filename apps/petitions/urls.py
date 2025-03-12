from django.urls import path

from .views import (
    # Petitions views
    PetitionListView,
    PetitionDetailView,
    PetitionUpdateView,
    PetitionDeleteView,
    PetitionCreateView,
    PetitionActivateView,
    # Department views
    DepartmentListView,
    DepartmentDetailView,
    DepartmentUpdateView,
    DepartmentDeleteView,
    DepartmentCreateView,
    # Company views
    CompanyListView,
    CompanyDetailView,
    CompanyUpdateView,
    CompanyDeleteView,
    CompanyCreateView,
    NotificationListView,
    NotificationMarkAsReadView,
)

app_name = "petitions"

urlpatterns = [
    # Petitions
    path("petitions/", PetitionListView.as_view(), name="petition-list"),
    path("petitions/<int:pk>/", PetitionDetailView.as_view(), name="petition-detail"),
    path(
        "petitions/create/",
        PetitionCreateView.as_view(),
        name="petition-create",
    ),
    path(
        "petitions/<int:pk>/update/",
        PetitionUpdateView.as_view(),
        name="petition-update",
    ),
    path(
        "petitions/<int:pk>/delete/",
        PetitionDeleteView.as_view(),
        name="petition-delete",
    ),
    path(
        "petitions/<int:petition_id>/activate/",
        PetitionActivateView.as_view(),
        name="petition-activate",
    ),
    # Departments
    path("departments/", DepartmentListView.as_view(), name="department-list"),
    path(
        "departments/<int:pk>/",
        DepartmentDetailView.as_view(),
        name="department-detail",
    ),
    path(
        "departments/create/",
        DepartmentCreateView.as_view(),
        name="department-create",
    ),
    path(
        "departments/<int:pk>/update/",
        DepartmentUpdateView.as_view(),
        name="department-update",
    ),
    path(
        "departments/<int:pk>/delete/",
        DepartmentDeleteView.as_view(),
        name="department-delete",
    ),
    # Companies
    path("companies/", CompanyListView.as_view(), name="company-list"),
    path(
        "companies/<int:pk>/",
        CompanyDetailView.as_view(),
        name="company-detail",
    ),
    path(
        "companies/create/",
        CompanyCreateView.as_view(),
        name="company-create",
    ),
    path(
        "companies/<int:pk>/update/",
        CompanyUpdateView.as_view(),
        name="company-update",
    ),
    path(
        "companies/<int:pk>/delete/",
        CompanyDeleteView.as_view(),
        name="company-delete",
    ),

    path("notifications/", NotificationListView.as_view(), name="notification-list"),
    path("notifications/<int:pk>/read/", NotificationMarkAsReadView.as_view(), name="notification-mark-as-read"),
]
