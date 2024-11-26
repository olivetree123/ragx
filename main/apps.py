from django.apps import AppConfig

from main.utils.milvus import MilvusClient


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        MilvusClient.init()
        return super().ready()
