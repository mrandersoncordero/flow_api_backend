from django.urls import path
from .views import (
    CommissionListView,
    CommissionCreateView,
    CommissionDetailView,
    CommissionUpdateView,
    CommissionDeleteView,
    CommissionAssignUsersView,
    CommissionActivateView,
)

app_name = "commissions"
urlpatterns = [
    path("commissions/", CommissionListView.as_view(), name="commission-list"),
    path(
        "commissions/create/", CommissionCreateView.as_view(), name="commission-create"
    ),
    path(
        "commissions/<int:pk>/",
        CommissionDetailView.as_view(),
        name="commission-detail",
    ),
    path(
        "commissions/<int:pk>/update/",
        CommissionUpdateView.as_view(),
        name="commission-update",
    ),
    path(
        "commissions/<int:pk>/delete/",
        CommissionDeleteView.as_view(),
        name="commission-delete",
    ),
    path(
        "commissions/<int:commission_id>/users/",
        CommissionAssignUsersView.as_view(),
        name="commission-assign-users",
    ),
    path(
        "commissions/<int:commission_id>/activate/",
        CommissionActivateView.as_view(),
        name="commission-activate",
    ),
]
