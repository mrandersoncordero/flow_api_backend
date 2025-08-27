from django.urls import path
from apps.api import views as api_views

# DRF Yasg
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Flow API",
        default_version="v1",  # 🔥 Cambiamos para usar versionamiento
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
    # Documentación Swagger con versión en la URL
    path(
        "swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),

    # Users URLs
    path("users/login/", api_views.UserLoginAPIView.as_view(), name="login"),
    path("users/singup/", api_views.UserSingUpAPIView.as_view(), name="signup"),
    path("users/verify/", api_views.AccountVerificationAPIView.as_view(), name="verify"),
    path("users/", api_views.UserListView.as_view(), name="user-list"),  # GET All
    path("users/<int:pk>/", api_views.UserDetailView.as_view(), name="user-detail"),  # GET by ID
    path(
        "users/<int:pk>/update/", api_views.UserUpdateView.as_view(), name="user-update"
    ),  # PUT / PATCH
    path(
        "users/<int:pk>/delete/", api_views.UserDeleteView.as_view(), name="user-delete"
    ),  # DELETE
    path(
        "users/<int:user_id>/add-to-group/<str:group_name>/",
        api_views.AddUserToGroupView.as_view(),
        name="add-to-group",
    ),
    path(
        "users/<int:user_id>/remove-from-group/<str:group_name>/",
        api_views.RemoveUserFromGroupView.as_view(),
        name="remove-from-group",
    ),
    # Human Resources URLs
    path(
        "human-resources/",
        api_views.HumanResourceCreateAPIView.as_view(),
        name="create-human-resource",
    ),
    path(
        "human-resources/me/",
        api_views.HumanResourceDetailUpdateAPIView.as_view(),
        name="detail-update-human-resource",
    ),
    
    # Commission URLs
    path("commissions/", api_views.CommissionListView.as_view(), name="commission-list"),
    path(
        "commissions/create/", api_views.CommissionCreateView.as_view(), name="commission-create"
    ),
    path(
        "commissions/<int:pk>/",
        api_views.CommissionDetailView.as_view(),
        name="commission-detail",
    ),
    path(
        "commissions/<int:pk>/update/",
        api_views.CommissionUpdateView.as_view(),
        name="commission-update",
    ),
    path(
        "commissions/<int:pk>/delete/",
        api_views.CommissionDeleteView.as_view(),
        name="commission-delete",
    ),
    path(
        "commissions/<int:commission_id>/users/",
        api_views.CommissionAssignUsersView.as_view(),
        name="commission-assign-users",
    ),
    path(
        "commissions/<int:commission_id>/activate/",
        api_views.CommissionActivateView.as_view(),
        name="commission-activate",
    ),
]
