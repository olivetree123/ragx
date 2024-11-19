import traceback
from django.core.management.base import BaseCommand

from main import models
from main.utils.log import get_logger
from main.utils.splitter_md import MarkdownSplitter

logger = get_logger("commands.make_paragraphs")


class Command(BaseCommand):
    help = """给文章生成段落"""

    def handle(self, *args, **options):
        while True:
            docs = list(models.Document.list_unparagraphed()[:100])
            if not docs:
                break
            for doc in docs:
                for part in MarkdownSplitter.split_text(doc.content):
                    try:
                        models.Paragraph.objects.get_or_create(
                            title=part.title,
                            content=part.content,
                            document_id=doc.id,
                            project_id=doc.project_id)
                    except Exception:
                        logger.error(traceback.format_exc())
