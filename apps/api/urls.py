from django.urls import path, re_path
from apps.api import views as api

# DRF Yasg
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Flow API",
        default_version="v1",
        description="API para la gestión de usuarios, peticiones y comisiones.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@flowapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

app_name = "api"

urlpatterns = [
    # Docs
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    # Users
    path("users/login/",  api.UserLoginAPIView.as_view(),  name="login"),
    path("users/signup/", api.UserSingUpAPIView.as_view(), name="signup"),
    path("users/verify/", api.AccountVerificationAPIView.as_view(), name="verify"),

    path("users/",              api.UserListView.as_view(),   name="user-list"),      # GET=list, POST=create (si tu vista lo soporta)
    path("users/<int:pk>/",     api.UserDetailView.as_view(), name="user-detail"),    # GET
    path("users/<int:pk>/",     api.UserUpdateView.as_view(), name="user-update"),    # PUT/PATCH (ideal unir en una sola vista)
    path("users/<int:pk>/",     api.UserDeleteView.as_view(), name="user-delete"),    # DELETE

    path("users/<int:user_id>/groups/<str:group_name>/add/",    api.AddUserToGroupView.as_view(),    name="user-group-add"),
    path("users/<int:user_id>/groups/<str:group_name>/remove/", api.RemoveUserFromGroupView.as_view(), name="user-group-remove"),

    # Human Resources
    path("human-resources/",     api.HumanResourceCreateAPIView.as_view(),       name="hr-create"),   # POST
    path("human-resources/me/",  api.HumanResourceDetailUpdateAPIView.as_view(), name="hr-me"),       # GET/PUT/PATCH

    # Commissions
    path("commissions/",                           api.CommissionListView.as_view(),   name="commission-list"),   # GET/POST
    path("commissions/<int:pk>/",                  api.CommissionDetailView.as_view(), name="commission-detail"), # GET/PUT/PATCH/DELETE
    path("commissions/<int:commission_id>/users/", api.CommissionAssignUsersView.as_view(), name="commission-assign-users"), # POST
    path("commissions/<int:commission_id>/activate/", api.CommissionActivateView.as_view(), name="commission-activate"),    # POST

    # Petitions
    path("petitions/",                      api.PetitionListView.as_view(),   name="petition-list"),   # GET/POST
    path("petitions/<int:pk>/",             api.PetitionDetailView.as_view(), name="petition-detail"), # GET/PUT/PATCH/DELETE
    path("petitions/<int:petition_id>/activate/", api.PetitionActivateView.as_view(), name="petition-activate"),  # POST

    # Departments
    path("departments/",          api.DepartmentListView.as_view(),   name="department-list"),   # GET/POST
    path("departments/<int:pk>/", api.DepartmentDetailView.as_view(), name="department-detail"), # GET/PUT/PATCH/DELETE

    # Companies
    path("companies/",          api.CompanyListView.as_view(),   name="company-list"),   # GET/POST
    path("companies/<int:pk>/", api.CompanyDetailView.as_view(), name="company-detail"), # GET/PUT/PATCH/DELETE

    # Notifications
    path("notifications/",              api.NotificationListView.as_view(),       name="notification-list"), # GET
    path("notifications/<int:pk>/read/", api.NotificationMarkAsReadView.as_view(), name="notification-read"), # POST/PATCH
]
