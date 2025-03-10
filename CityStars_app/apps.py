from django.apps import AppConfig


class CitystarsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CityStars_app'

    def ready(self):
        import CityStars_app.signals
