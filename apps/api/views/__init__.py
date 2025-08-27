# __init__.py
from apps.api.views.comissions import (
    CommissionListView,
    CommissionCreateView,
    CommissionDetailView,
    CommissionUpdateView,
    CommissionDeleteView,
    CommissionAssignUsersView,
    CommissionActivateView,
)
from apps.api.views.users import (
    UserLoginAPIView,
    UserSingUpAPIView,
    AccountVerificationAPIView,
    UserListView,
    UserDetailView,
    UserUpdateView,
    UserDeleteView,
    RemoveUserFromGroupView,
    AddUserToGroupView,
)
from apps.api.views.human_resource import (
    HumanResourceCreateAPIView,
    HumanResourceDetailUpdateAPIView,
)

__all__ = [
    # Users
    UserLoginAPIView,
    UserSingUpAPIView,
    AccountVerificationAPIView,
    UserListView,
    UserDetailView,
    UserUpdateView,
    UserDeleteView,
    RemoveUserFromGroupView,
    AddUserToGroupView,
    # Human Resources
    HumanResourceCreateAPIView,
    HumanResourceDetailUpdateAPIView,
    AddUserToGroupView,
    # Comisions
    CommissionListView,
    CommissionCreateView,
    CommissionDetailView,
    CommissionUpdateView,
    CommissionDeleteView,
    CommissionAssignUsersView,
    CommissionActivateView,
]