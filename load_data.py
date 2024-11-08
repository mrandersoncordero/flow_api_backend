import os
from datetime import timedelta
import django
from django.db import IntegrityError

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flow.settings")
django.setup()

# Models
from tasks.models import Department, TaskStatus, Task, Company
from users.models import User


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
        )
        superuser.save()
        print("\nSuccessfully created superuser.")
    else:
        print("Superuser already exists. Skipping creation.")


def main():

    create_superuser()

    data_department = [
        {"name": "Service Pack", "description": ""},
        {"name": "Infraestructura", "description": ""},
        {"name": "Social Media", "description": ""},
        {"name": "Sistemas", "description": ""},
        {"name": "Desarrollo Web", "description": ""},
        {"name": "Centro de Servicio EPSON", "description": ""},
    ]

    load_data(
        data_department,
        model=Department,
        unique_fields=["name"],
        message=["Creating department", "Department successfully created"],
    )

    data_taskstatus = [
        {"name": "Completado"},
        {"name": "En Progreso"},
        {"name": "No Iniciado"},
    ]

    load_data(
        data_taskstatus,
        model=TaskStatus,
        unique_fields=["name"],
        message=["Creating TaskStatus", "TaskStatus successfully created"],
    )

    data_companies = [
        {"name": "Nardi Industrias Barquisimeto, C.A."},
        {"name": "Nardi Industrias Trujillo, C.A."},
        {"name": "Transporte San Gregorio, C.A."},
        {"name": "Direccion General de Empresas, C.A."},
        {"name": "Distribucion & Servicios Industriales, C.A."},
        {"name": "Procesadora de Silice, C.A."},
        {"name": "Franar, C.A."},
        {"name": "Branar, C.A."},
    ]

    load_data(
        data_companies,
        model=Company,
        unique_fields=["name"],
        message=["Creating Company", "Company successfully created"],
    )

    data_task = []
    departments = Department.objects.all()
    task_status = TaskStatus.objects.get(pk=3)
    user = User.objects.first()

    company_id = 1

    for department in departments:
        data_task.append(
            {
                "user": user,
                "title": f"Tarea 1 en {department.name}",
                "description": f"Descripción de la tarea 1 en {department.name}",
                "department": department,
                "company": Company.objects.get(pk=company_id),
                "status": task_status,
                "hours": timedelta(hours=2),
            }
        )
        data_task.append(
            {
                "user": user,
                "title": f"Tarea 2 en {department.name}",
                "description": f"Descripción de la tarea 2 en {department.name}",
                "department": department,
                "company": Company.objects.get(pk=company_id),
                "status": task_status,
                "hours": timedelta(hours=3),
            }
        )
        company_id += 1
    load_data(
        data_task,
        model=Task,
        message=["Creating Task", "Tasks successfully created"],
    )


if __name__ == "__main__":
    main()
