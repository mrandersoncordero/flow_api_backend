from django.db.models.signals import post_save
from django.dispatch import receiver
from petitions.models import Petition
from petitions.models import Notification
from users.models import HumanResource, ClientCompany
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@receiver(post_save, sender=Petition)
def create_notification(sender, instance, created, **kwargs):
    """Crea una notificación y envía un correo cuando se crea o actualiza una petición."""

    recipients = set()  # 🔥 Usamos un `set()` para evitar duplicados
    message = None

    if created:
        message = f"Se ha creado una nueva petición: {instance.title}"
    elif instance.status_approval in ["AP", "NP", "DN"]:
        message = f"La petición '{instance.title}' ha cambiado de estado a {instance.get_status_approval_display()}."

    if message:
        # 🔥 1. ADMIN: Ver TODAS las peticiones
        admin_users = HumanResource.objects.filter(user__groups__name="Admin").values_list("user", flat=True)
        recipients.update(admin_users)

        # 🔥 2. MANAGER: Solo notificaciones de su departamento
        if instance.department:
            manager_users = HumanResource.objects.filter(
                department=instance.department, user__groups__name="Manager"
            ).values_list("user", flat=True)
            recipients.update(manager_users)

        # 🔥 3. CLIENT: Solo notificaciones de su empresa
        if instance.company:
            client_users = HumanResource.objects.filter(
                company=instance.company, user__groups__name="Client"
            ).values_list("user", flat=True)
            recipients.update(client_users)

        # 🔥 4. CLIENTS con múltiples empresas
        client_company_users = ClientCompany.objects.filter(
            company=instance.company
        ).values_list("human_resource__user", flat=True)
        recipients.update(client_company_users)

        # 🔥 Crear Notificaciones en Base de Datos
        notifications = [
            Notification(recipient_id=user_id, petition=instance, message=message)
            for user_id in recipients
        ]
        Notification.objects.bulk_create(notifications)

        # 🔥 Enviar Emails a los Usuarios
        # 🔥 Enviar Emails con Templates HTML
        for user_id in recipients:
            user = HumanResource.objects.get(user_id=user_id).user  
            if user.email:  # 🔥 Solo enviar si tiene email válido
                context = {
                    "user": user,
                    "petition": instance,
                    "message": message,
                    "petition_url": f"http://localhost/task-flow/views/peticiones_detalle.php?petition_id={instance.id}",  # 🔥 Enlace a la petición
                }
                
                subject = "Nueva Notificación - Peticiones"
                text_content = f"{message}\n\nVer más en: {context['petition_url']}"
                html_content = render_to_string("emails/notification_email.html", context)

                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email]
                )
                email.attach_alternative(html_content, "text/html")
                email.send(fail_silently=True)  # 🔥 No detener ejecución si falla el email
