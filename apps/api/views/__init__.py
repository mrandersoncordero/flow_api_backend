# apps/api/views/__init__.py

# Users
from .users import (
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

# Human Resources
from .human_resource import (
    HumanResourceCreateAPIView,
    HumanResourceDetailUpdateAPIView,
)

# Commissions
from .comissions import (
    CommissionListView,
    CommissionCreateView,
    CommissionDetailView,
    CommissionUpdateView,
    CommissionDeleteView,
    CommissionAssignUsersView,
    CommissionActivateView,
)

# Petitions
from .petition_view import (
    PetitionListView,
    PetitionDetailView,
    PetitionUpdateView,
    PetitionDeleteView,
    PetitionCreateView,
    PetitionActivateView,
)

# Departments
from .department_view import (
    DepartmentListView,
    DepartmentDetailView,
    DepartmentUpdateView,
    DepartmentDeleteView,
    DepartmentCreateView,
)

# Companies
from .company_view import (
    CompanyListView,
    CompanyDetailView,
    CompanyUpdateView,
    CompanyDeleteView,
    CompanyCreateView,
)

# Notifications
from .notification_view import (
    NotificationListView,
    NotificationMarkAsReadView,
)

__all__ = [
    # Users
    "UserLoginAPIView", "UserSingUpAPIView", "AccountVerificationAPIView",
    "UserListView", "UserDetailView", "UserUpdateView", "UserDeleteView",
    "RemoveUserFromGroupView", "AddUserToGroupView",

    # Human Resources
    "HumanResourceCreateAPIView", "HumanResourceDetailUpdateAPIView",

    # Commissions
    "CommissionListView", "CommissionCreateView", "CommissionDetailView",
    "CommissionUpdateView", "CommissionDeleteView",
    "CommissionAssignUsersView", "CommissionActivateView",

    # Petitions
    "PetitionListView", "PetitionDetailView", "PetitionUpdateView",
    "PetitionDeleteView", "PetitionCreateView", "PetitionActivateView",

    # Departments
    "DepartmentListView", "DepartmentDetailView", "DepartmentUpdateView",
    "DepartmentDeleteView", "DepartmentCreateView",

    # Companies
    "CompanyListView", "CompanyDetailView", "CompanyUpdateView",
    "CompanyDeleteView", "CompanyCreateView",

    # Notifications
    "NotificationListView", "NotificationMarkAsReadView",
]
