from django.db import transaction
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
            logger.info(f"len docs = {len(docs)}")
            if not docs:
                break
            for doc in docs:
                ps = []
                for part in MarkdownSplitter.split_text(doc.content):
                    if not part.title:
                        continue
                    logger.info(f"paragraph={part.title}")
                    p = models.Paragraph(title=part.title,
                                         content=part.content,
                                         document_id=doc.id,
                                         project_id=doc.project_id)
                    ps.append(p)
                with transaction.atomic():
                    models.Paragraph.objects.bulk_create(ps)
                    models.Document.update_paragraphed(doc.id)
                logger.info(f"doc={doc.title} 分段完成")
