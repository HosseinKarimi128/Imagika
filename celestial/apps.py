from django.apps import AppConfig
from django.db.models.signals import post_save


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'celestial'
    # def ready(self):
    #     from celestial.models import update_post_score
    #     post_save.connect(update_post_score, sender=Post)
