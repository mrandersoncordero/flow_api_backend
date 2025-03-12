from django.apps import AppConfig


class PetitionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'petitions'

    def ready(self):
        import petitions.signals