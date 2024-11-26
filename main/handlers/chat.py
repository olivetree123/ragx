from typing import Optional

from pymilvus import (
    AnnSearchRequest,
    WeightedRanker,
    RRFRanker,
    SearchResult,
    Hits,
)
from ninja import Schema, Field
from openai import OpenAI

from main import (
    dao,
    models,
    params,
    results,
)
from main.response import (
    OkResponse,
    FailResponse,
    APIStatus,
)
from main.md.current import current_project
from main.utils.embedding import EmbeddingFunction
from main.utils.es import es_search
from main.utils.milvus import MilvusClient
from main.utils.reranker import rerank_service, rerank
from main.utils.llm import check_relatedness, check_relatedness_v2
from main.utils.ollama import OllamaClient
from main.utils.log import get_logger
from main.utils.timer import Timer

logger = get_logger(name="handlers.chat")


# 发送消息请求模型
class SendMessageRequest(Schema):
    session_id: int
    content: str


# method = Milvus-ES-Rerank
def ChatV1Handler(request, message: SendMessageRequest):
    logger.info(f"query={message.content}")
    method = "Milvus-ES-Rerank"
    # 1. ES关键字查询
    titles = es_search(message.content)

    names = [title for title in titles]
    paragraphs = dao.Paragraph.filter_by_doc_names(
        names=names, project_id=current_project())
    paragraph_id_list = [p.id for p in paragraphs]

    # 2. 从向量数据库查询
    hits: Hits = dao.Milvus.hybrid_search(text=message.content, limit=40)

    # 3. 组合查询结果
    paragraph_id_list += [hit.get("paragraph_id") for hit in hits]
    paragraphs = models.Paragraph.list_by_ids(ids=paragraph_id_list,
                                              project_id=current_project())

    paragraphs = [{
        "id": p.id,
        "title": p.title,
        "content": p.content,
        "doc_id": p.document_id,
        "doc_title": p.document.title,
    } for p in paragraphs]

    result = [{
        "query": message.content,
        "method": method,
        "paragraph_id": p["id"],
        "paragraph_title": p["title"],
        "paragraph_content": p["content"],
        "doc_id": p["doc_id"],
        "doc_title": p["doc_title"],
        "project_id": current_project(),
    } for p in paragraphs]

    paragraph_titles = [p["title"] for p in paragraphs]

    # 4. 重排序，按段落标题重排序
    with Timer(name="重排序"):
        scores = rerank(message.content, paragraph_titles)
        for i, score in enumerate(scores):
            result[i]["rerank_score"] = score
            # if score < -0.5:
            #     result[i] = None
            # else:
            #     result[i]["rerank_score"] = score

    result = [item for item in result if item]
    reports = [models.Report(**item) for item in result]
    models.Report.objects.bulk_create(reports)
    return OkResponse()
