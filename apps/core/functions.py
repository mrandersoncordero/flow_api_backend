def filter_queryset_by_group(queryset, user):
    """Filtra los usuarios según el grupo del usuario autenticado."""

    if user.groups.filter(name="Admin").exists():
        return queryset  # 🔥 Admin ve todos los usuarios

    elif user.groups.filter(name="Manager").exists():
        return queryset.filter(
            department__id=user.human_resource.department.id
        )  # 🔥 Managers ven empleados de su departamento
    
    elif user.groups.filter(name="Employee").exists():
        return queryset.filter(id=user.id)  # 🔥 Employees solo ven su propio perfil

    elif user.groups.filter(name="Client").exists():
        return queryset.filter(
            company__id=user.human_resource.company.id
        )

    return queryset.none()  # 🔥 Si el usuario no pertenece a un grupo, no ve nada



def filter_queryset_user_by_group(queryset, user):
    """Filtra los usuarios según el grupo del usuario autenticado."""

    if user.groups.filter(name="Admin").exists():
        return queryset  # 🔥 Admin ve todos los usuarios

    elif user.groups.filter(name="Manager").exists():
        return queryset.filter(
            human_resource__department=user.human_resource.department
        )  # 🔥 Managers ven empleados de su departamento

    elif user.groups.filter(name="Employee").exists():
        return queryset.filter(id=user.id)  # 🔥 Employees solo ven su propio perfil

    elif user.groups.filter(name="Client").exists():
        return queryset.filter(
            human_resource__company=user.human_resource.company
        )  # 🔥 Clients solo ven su perfil y si pertenece a su empresa

    return queryset.none()  # 🔥 Si el usuario no pertenece a un grupo, no ve nada
