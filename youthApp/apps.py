from django.apps import AppConfig


class YouthappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'youthApp'

    def ready(self):
        import youthApp.signals     