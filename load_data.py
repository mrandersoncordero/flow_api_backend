# load_data.py

import os
from datetime import time
import django

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flow.settings")
django.setup()

# Models
from tasks.models import Department, TaskStatus, Task
from users.models import User


def load_data(data, model, message=["Creating", "Created Succesfully"]):
    """Funcion para insertar datos en una tabla.

    Parametros posicionales
    data -- list una variable que contiene una lista de diccionarios.
    model -- obj modelo al que se insertaran los datos.
    message -- list mensajes
    """

    if model is None:
        raise ValueError('ERROR: El parametro "model" es obligatorio')

    print("*" * 5, f"{message[0].title()}", "*" * 5)
    for d in data:
        obj = model(**d)
        print("-", obj)
        obj.save()
    print("*" * 5, f"{message[1]}", "*" * 5, end="\n\n")


def create_superuser():
    superuser = User.objects.create_superuser(
        username="admin",
        first_name="Administrator",
        last_name="",
        password="root",
        email="admin@email.com",
    )
    # group = Group.objects.get(name='admins')  # Obtén la instancia del grupo
    # superuser.groups.add(group)
    superuser.save()
    print("\nSuccessfully created superuser.")


def main():

    create_superuser()

    data_department = [
        {"name": "Service Pack", "description": ""},
        {"name": "Infraestrucutra", "description": ""},
        {"name": "Social Media", "description": ""},
        {"name": "Sistemas", "description": ""},
        {"name": "Desarrollo Web", "description": ""},
        {"name": "Centro de Servicio EPSON", "description": ""},
    ]

    load_data(
        data_department,
        model=Department,
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
        message=["Creating TaskStatus", "TaskStatus succesfully created"],
    )

    data_task = []
    departments = Department.objects.all()
    task_status = TaskStatus.objects.get(pk=3)
    user = User.objects.first()

    for department in departments:
        data_task.append(
            {
                "user": user,
                "title": f"Tarea 1 en {department.name}",
                "description": f"Descripción de la tarea 1 en {department.name}",
                "department": department,
                "status": task_status,
                "hours": time(2, 0),  # 2 horas
            }
        )
        data_task.append(
            {
                "user": user,
                "title": f"Tarea 2 en {department.name}",
                "description": f"Descripción de la tarea 2 en {department.name}",
                "department": department,
                "status": task_status,
                "hours": time(3, 0),  # 3 horas
            }
        )

    load_data(
        data_task,
        model=Task,
        message=["Creating Task", "Tasks successfully created"],
    )


if __name__ == "__main__":
    main()
