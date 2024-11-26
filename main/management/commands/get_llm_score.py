from django.db import transaction
from django.core.management.base import BaseCommand

from main import models
from main.utils.log import get_logger
from main.utils.llm import check_relatedness

logger = get_logger("commands.make_paragraphs")


class Command(BaseCommand):
    help = """给文章生成段落"""

    def handle(self, *args, **options):
        items = models.Report.objects.values("query").distinct()
        for item in items:
            query = item["query"]
            rs = models.Report.objects.filter(
                query=query).values("doc_id").distinct()
            doc_ids = [r["doc_id"] for r in rs]
            docs = models.Document.list_by_ids(doc_ids)
            for doc in docs:
                is_related = check_relatedness(query=query,
                                               content=doc.content)
                llm_score = 1 if is_related else -1
                models.Report.objects.filter(
                    query=query, doc_id=doc.id).update(llm_score=llm_score)
