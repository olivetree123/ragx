import traceback

from celery import shared_task

from main import models
from main.utils.log import get_logger
from main.utils.milvus import Milvus
from main.utils.embedding import EmbeddingFunction
from main.utils.splitter_md import MarkdownSplitter, MarkChunkHandler

logger = get_logger("ragx.tasks")


@shared_task(ignore_result=True)
def doc_handle(doc_id, doc_content, project_id):
    """给文章分段，并生成向量保存到向量数据库"""
    for part in MarkdownSplitter.split_text(doc_content):
        try:
            models.Paragraph.objects.get_or_create(title=part.title,
                                                   content=part.content,
                                                   document_id=doc_id,
                                                   project_id=project_id)

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
        except Exception:
            logger.error(f"Failed to handle doc, doc_id: {doc_id}")
            logger.error(traceback.format_exc())


@shared_task(ignore_result=True)
def doc_delete(doc_id):
    """删除文章时，删除文章的所有段落和向量"""
    try:
        Milvus.collection.delete(f"document_id in {[doc_id]}")
        models.Paragraph.objects.filter(document_id=doc_id).delete()
    except Exception:
        logger.error(f"Failed to delete doc, doc_id: {doc_id}")
        logger.error(traceback.format_exc())
