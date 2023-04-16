from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'celestial'
    app_label  = 'celestial'
    verbose_name = 'A celestial'
