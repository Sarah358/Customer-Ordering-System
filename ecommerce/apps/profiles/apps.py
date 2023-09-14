from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ecommerce.apps.profiles"

    def ready(self):
        from ecommerce.apps.profiles import signals
