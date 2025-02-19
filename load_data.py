import os
from datetime import timedelta
import django
from django.db import IntegrityError

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flow.settings")
django.setup()

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
                # Verificar si el registro ya existe basado en campos únicos
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
            if message[0] == "Creating Commission":
                obj.users.set([User.objects.get(pk=2)])
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
        superuser.save()
        print("\nSuccessfully created superuser.")
    else:
        print("Superuser already exists. Skipping creation.")


def create_user_test():
    if not User.objects.filter(username="test").exists():
        user = User.objects.create(
            username="test",
            first_name="Jhon",
            last_name="Dae",
            password="test",
            email="test@email.com",
            is_verified=True,
        )
        user.save()
        print("\nSuccessfully created test user.\n")

        human_resource = HumanResource.objects.create(
            user=user,
            biography="Biografia del usuario test.",
            phone_number="9898989898",
            department=Department.objects.get(pk=5),
            company=Company.objects.get(pk=1),
        )
        human_resource.save()
        print("Test user human resource successfully created.\n")
    else:
        print("User already exists. Skipping creation.")


def main():

    data_department = [
        {"name": "Service Pack"},
        {"name": "Infraestructura"},
        {"name": "Social Media"},
        {"name": "Sistemas"},
        {"name": "Desarrollo Web"},
        {"name": "Centro de Servicio EPSON"},
    ]

    load_data(
        data_department,
        model=Department,
        unique_fields=["name"],
        message=["Creating department", "Department successfully created"],
    )

    data_companies = [
        {"name": "Branar, C.A."},
        {"name": "Franar, C.A."},
        {"name": "Procesadora de Silice, C.A."},
        {"name": "Transporte San Gregorio, C.A."},
        {"name": "Nardi Industrias Trujillo, C.A."},
        {"name": "Nardi Industrias Barquisimeto, C.A."},
        {"name": "Direccion General de Empresas, C.A."},
        {"name": "Distribucion & Servicios Industriales, C.A."},
    ]

    load_data(
        data_companies,
        model=Company,
        unique_fields=["name"],
        message=["Creating Company", "Company successfully created"],
    )

    create_superuser()

    create_user_test()

    data_petitions = [
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
            "user": User.objects.get(pk=2),
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

    load_data(
        data_petitions,
        model=Petition,
        message=["Creating Petition", "Petition successfully created"],
    )
    users = User.objects.filter(id__in=[2])
    data_commissions = [
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

    # Crea las comisiones
    load_data(
        data_commissions,
        model=Commission,
        message=["Creating Commission", "Commission successfully created"],
    )

    # data_task = []
    # departments = Department.objects.all()
    # task_status = TaskStatus.objects.get(pk=3)
    # user = User.objects.first()

    # company_id = 1

    # for department in departments:
    #     data_task.append(
    #         {
    #             "user": user,
    #             "title": f"Tarea 1 en {department.name}",
    #             "description": f"Descripción de la tarea 1 en {department.name}",
    #             "department": department,
    #             "company": Company.objects.get(pk=company_id),
    #             "status": task_status,
    #             "hours": timedelta(hours=2),
    #         }
    #     )
    #     data_task.append(
    #         {
    #             "user": user,
    #             "title": f"Tarea 2 en {department.name}",
    #             "description": f"Descripción de la tarea 2 en {department.name}",
    #             "department": department,
    #             "company": Company.objects.get(pk=company_id),
    #             "status": task_status,
    #             "hours": timedelta(hours=3),
    #         }
    #     )
    #     company_id += 1
    # load_data(
    #     data_task,
    #     model=Task,
    #     message=["Creating Task", "Tasks successfully created"],
    # )


if __name__ == "__main__":
    main()
