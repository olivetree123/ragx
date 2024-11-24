from django.core.management.base import BaseCommand

from main import models
from main.utils.log import get_logger
from main.utils.es import es_save

logger = get_logger("commands.make_embeddings")


class Command(BaseCommand):
    help = """上传到ES"""

    def handle(self, *args, **options):
        for doc in models.Document.objects.all():
            es_save(doc.json(exclude=["is_paragraphed"]))
