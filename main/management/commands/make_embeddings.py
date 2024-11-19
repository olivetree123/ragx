from django.core.management.base import BaseCommand

from main import models
from main.utils.log import get_logger
from main.utils.milvus import Milvus
from main.utils.embedding import EmbeddingFunction
from main.utils.splitter_md import MarkChunkHandler

logger = get_logger("commands.make_embeddings")


class Command(BaseCommand):
    help = """生成段落的向量"""

    def handle(self, *args, **options):
        while True:
            parts = list(models.Paragraph.list_unembeddinged()[:1000])
            if not parts:
                break
            for part in parts:
                text = part.title + "\n" + part.content
                _sentences = MarkChunkHandler.handle([text])
                documents += [part.document_id] * len(_sentences)
                parts += [part.id] * len(_sentences)
                sentences += _sentences
                if not sentences:
                    continue
                embeddings = EmbeddingFunction.call(sentences)
                Milvus.collection.insert([
                    sentences,
                    embeddings["sparse"],
                    embeddings["dense"],
                    parts,
                    documents,
                ])
                models.Paragraph.update_embeddinged(paragraph_id=part.id)
