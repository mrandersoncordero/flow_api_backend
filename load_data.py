import os
import django

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flow.settings")
django.setup()

from django.db import IntegrityError
from django.contrib.auth.models import Group

# Models
from petitions.models import Department, Company, Petition
from commissions.models import Commission
from users.models import User
from users.models.human_resources_model import HumanResource


def load_data(
    data, model, unique_fields=None, message=["Creating", "Created Successfully"]
):
    """Funcion para insertar datos en una tabla.

    Parametros posicionales:
    data -- list una variable que contiene una lista de diccionarios.
    model -- obj modelo al que se insertaran los datos.
    unique_fields -- list lista de campos que deben ser únicos.
    message -- list mensajes
    """

    if model is None:
        raise ValueError('ERROR: El parametro "model" es obligatorio')

    print("*" * 5, f"{message[0].title()}", "*" * 5)
    for d in data:
        try:
            if unique_fields:
                filter_kwargs = {
                    field: d[field] for field in unique_fields if field in d
                }
                if model.objects.filter(**filter_kwargs).exists():
                    print(
                        f"- {model.__name__} with {filter_kwargs} already exists. Skipping..."
                    )
                    continue

            obj = model(**d)
            obj.save()
            print(f"- {obj} created successfully.")

        except IntegrityError as e:
            print(f"Error: {e} - {d}")
        except Exception as e:
            print(f"Unexpected error: {e} - {d}")

    print("*" * 5, f"{message[1]}", "*" * 5, end="\n\n")


def create_superuser():
    if not User.objects.filter(username="admin").exists():
        superuser = User.objects.create_superuser(
            username="admin",
            first_name="Administrator",
            last_name="",
            password="root",
            email="admin@email.com",
            is_verified=True,
        )
        superuser.groups.add(Group.objects.get(name="Admin"))
        superuser.save()
        print("\nSuccessfully created superuser.")
    else:
        print("Superuser already exists. Skipping creation.")


def main():

    data_department = [  # Definir los departamentos a crear
        {"name": "Service Pack"},
        {"name": "Infraestructura"},
        {"name": "Social Media"},
        {"name": "Sistemas"},
        {"name": "Desarrollo Web"},
        {"name": "Centro de Servicio EPSON"},
    ]

    load_data(  # Insertar departamentos en la base de datos
        data_department,
        model=Department,
        unique_fields=["name"],
        message=["Creating department", "Department successfully created"],
    )

    data_companies = [  # Definir las empresas a crear
        {"name": "Branar, C.A."},
        {"name": "Franar, C.A."},
        {"name": "Procesadora de Silice, C.A."},
        {"name": "Transporte San Gregorio, C.A."},
        {"name": "Nardi Industrias Trujillo, C.A."},
        {"name": "Nardi Industrias Barquisimeto, C.A."},
        {"name": "Direccion General de Empresas, C.A."},
        {"name": "Distribucion & Servicios Industriales, C.A."},
    ]

    load_data(  # Insertar empresas en la base de datos
        data_companies,
        model=Company,
        unique_fields=["name"],
        message=["Creating Company", "Company successfully created"],
    )

    users_data = [  # Definir los usuarios a crear
        {
            "username": "client1",
            "first_name": "Carlos",
            "last_name": "Perez",
            "email": "client1@email.com",
            "is_verified": True,
        },
        {
            "username": "client2",
            "first_name": "Maria",
            "last_name": "Gomez",
            "email": "client2@email.com",
            "is_verified": True,
        },
        {
            "username": "client3",
            "first_name": "Luis",
            "last_name": "Fernandez",
            "email": "client3@email.com",
            "is_verified": True,
        },
        {
            "username": "manager1",
            "first_name": "Ana",
            "last_name": "Torres",
            "email": "manager1@email.com",
            "is_verified": True,
        },
        {
            "username": "manager2",
            "first_name": "Pedro",
            "last_name": "Ramirez",
            "email": "manager2@email.com",
            "is_verified": True,
        },
    ]

    human_resource_data = [
        {"user": "client1", "department": None, "company": 2},
        {"user": "client2", "department": None, "company": 2},
        {"user": "client3", "department": None, "company": 3},
        {"user": "manager1", "department": 2, "company": 1},
        {"user": "manager2", "department": 5, "company": 1},
    ]

    # Crear Grupos
    admin_group, _ = Group.objects.get_or_create(name="Admin")
    manager_group, _ = Group.objects.get_or_create(name="Manager")
    employee_group, _ = Group.objects.get_or_create(name="Employee")
    client_group, _ = Group.objects.get_or_create(name="Client")

    create_superuser()  # Crear superusuario

    load_data(  # Insertar usuarios en la base de datos
        users_data,
        User,
        unique_fields=["username"],
        message=["Creating Users", "Users Created Successfully"],
    )

    # Asignar grupos y crear HumanResource para cada usuario
    for user_data in users_data:
        user = User.objects.get(username=user_data["username"])
        if "client" in user.username:
            group = Group.objects.get(name="Client")
        else:
            group = Group.objects.get(name="Manager")

        user.groups.add(group)
        user.set_password(user.username)  # Asignar la contraseña igual al username
        user.save()

        # Crear HumanResource
        human_resource = HumanResource.objects.create(
            user=user,
            biography=f"Biografia del usuario {user.username}.",
            phone_number="9898989898",
            company=Company.objects.get(pk=1),
        )
        if "client" in user.username:
            human_resource.company = Company.objects.get(pk=2)
        else:
            human_resource.company = Company.objects.get(pk=1)
            human_resource.department = Department.objects.get(pk=5)
        human_resource.save()
        print(f"Human resource for {user.username} successfully created.")

    data_petitions = [  # Definir las peticiones a crear
        {
            "is_main": True,
            "title": "Mantenimiento de Equipos NIB",
            "description": "Mantenimiento de Equipos NIB",
            "priority": "HG",
            "status_approval": "WT",
            "department": Department.objects.get(pk=2),
            "company": Company.objects.get(pk=6),
            "user": User.objects.get(pk=1),
        },
        {
            "is_main": True,
            "title": "Mantenimiento de Equipos NIT",
            "description": "Mantenimiento de Equipos NIT",
            "priority": "HG",
            "status_approval": "AP",
            "department": Department.objects.get(pk=2),
            "company": Company.objects.get(pk=5),
            "user": User.objects.get(pk=1),
        },
        {
            "is_main": True,
            "title": "Peticion 3",
            "description": "Peticion 3",
            "priority": "HG",
            "status_approval": "AP",
            "department": Department.objects.get(pk=1),
            "company": Company.objects.get(pk=1),
            "user": User.objects.get(pk=1),
        },
        {
            "is_main": False,
            "title": "Cambiar aplicacion de peticiones",
            "description": "Cambiar aplicacion de peticiones",
            "priority": "HG",
            "status_approval": "AP",
            "department": Department.objects.get(pk=5),
            "company": Company.objects.get(pk=1),
            "user": User.objects.get(pk=5),
        },
        {
            "is_main": False,
            "title": "Cableado franar",
            "description": "Cableado franar",
            "priority": "HG",
            "status_approval": "AP",
            "department": Department.objects.get(pk=2),
            "company": Company.objects.get(pk=2),
            "user": User.objects.get(pk=2),
        },
    ]

    load_data(  # Insertar peticiones en la base de datos
        data_petitions,
        model=Petition,
        message=["Creating Petition", "Petition successfully created"],
    )

    data_commissions = [  # Definir las comisiones a crear
        {
            "description": "Cambiar Base de datos",
            "status": "OPEN",
            "petition": Petition.objects.get(pk=4),
        },
        {
            "description": "Cambiar API CRUD",
            "status": "OPEN",
            "petition": Petition.objects.get(pk=4),
        },
        {
            "description": "TEST api",
            "status": "OPEN",
            "petition": Petition.objects.get(pk=4),
        },
        {
            "description": "Frontend",
            "status": "OPEN",
            "petition": Petition.objects.get(pk=4),
        },
    ]

    load_data(  # Insertar comisiones en la base de datos
        data_commissions,
        model=Commission,
        message=["Creating Commission", "Commission successfully created"],
    )


if __name__ == "__main__":
    main()
