from django.apps import AppConfig
from django.db.models.signals import post_save
# from core.models import Post


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    # def ready(self):
    #     from core.models import update_post_score
    #     post_save.connect(update_post_score, sender=Post)
