from django.core.management.base import BaseCommand

from main import models
from main.utils.log import get_logger
from main.utils.milvus import MilvusClient
from main.utils.embedding import EmbeddingFunction
from main.utils.splitter_md import MarkChunkHandler

logger = get_logger("commands.make_embeddings")


class Command(BaseCommand):
    help = """生成段落的向量"""

    def handle(self, *args, **options):
        # Milvus.drop_collection("ragx")
        MilvusClient.init()
        while True:
            ps = list(models.Paragraph.list_unembeddinged()[:1000])
            if not ps:
                break
            logger.info(f"len paragraphs = {len(ps)}")
            for part in ps:
                # logger.info(f"paragraph={part.title}")
                text = part.title + "\n" + part.content
                _sentences = MarkChunkHandler.handle([text])
                documents = [part.document_id] * len(_sentences)
                parts = [part.id] * len(_sentences)
                sentences = _sentences
                if not sentences:
                    continue
                embeddings = EmbeddingFunction.call(sentences)
                try:
                    MilvusClient.collection.insert([
                        sentences,
                        embeddings["sparse"],
                        embeddings["dense"],
                        parts,
                        documents,
                    ])
                    models.Paragraph.update_embeddinged(paragraph_id=part.id)
                except Exception as e:
                    logger.error(f"title={part.title}")
                    logger.error(f"error={e}")
                    models.Paragraph.update_embeddinged(paragraph_id=part.id)
