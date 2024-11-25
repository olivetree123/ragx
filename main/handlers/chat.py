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
from main.utils.milvus import Milvus
from main.utils.reranker import rerank_service
from main.utils.openai import check_relatedness
from main.utils.ollama import OllamaClient
from main.utils.log import get_logger

logger = get_logger(name="handlers.chat")


# 发送消息请求模型
class SendMessageRequest(Schema):
    session_id: int
    content: str


# method = Milvus-ES-Rerank
def ChatV1Handler(request, message: SendMessageRequest):
    method = "Milvus-ES-Rerank"
    # 1. ES关键字查询
    titles = es_search(message.content)
    names = [title for title in titles]
    paragraphs = dao.Paragraph.filter_by_doc_names(names=names)
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

    report = [{
        "query": message.content,
        "method": method,
        "paragraph_id": p["id"],
        "paragraph_title": p["title"],
        "paragraph_content": p["content"],
        "doc_id": p["doc_id"],
        "doc_title": p["doc_title"],
        "project_id": current_project(),
    } for p in paragraphs]

    result_paragraph_titles = [p["title"] for p in paragraphs]

    # 4. 重排序，按段落标题重排序
    scores = rerank_service(message.content, result_paragraph_titles)
    for i, score in enumerate(scores):
        if score < -0.5:
            report[i] = None
            # result_paragraph_contents[i] = ""

    report = [item for item in report if item]

    # 使用大模型过滤结果
    positive = negative = 0
    for item in report:
        item["method"] = f"{method}-gpt4omini"
        relatedness = check_relatedness(item["doc_title"], message.content)
        # item["score"] = 1 if relatedness else -1
        if relatedness:
            positive += 1
            item["score"] = 1
        else:
            negative += 1
            item["score"] = -1
    models.Report.objects.bulk_create(report)

    logger.info(f"method={method}-gpt4omini, "
                "positive={positive}, "
                "negative={negative}")

    # 使用大模型过滤结果
    positive = negative = 0
    for item in report:
        item["method"] = f"{method}-qwen2.5:7b"
        relatedness = OllamaClient.check_relatedness(item["doc_title"],
                                                     message.content,
                                                     model="qwen2.5:7b")
        if relatedness:
            positive += 1
            item["score"] = 1
        else:
            negative += 1
            item["score"] = -1
    models.Report.objects.bulk_create(report)

    logger.info(f"method={method}-qwen2.5:7b, "
                "positive={positive}, "
                "negative={negative}")

    # 使用大模型过滤结果
    positive = negative = 0
    for item in report:
        item["method"] = f"{method}-llama3.2:3b"
        relatedness = OllamaClient.check_relatedness(item["doc_title"],
                                                     message.content,
                                                     model="llama3.2:3b")
        if relatedness:
            positive += 1
            item["score"] = 1
        else:
            negative += 1
            item["score"] = -1
    models.Report.objects.bulk_create(report)

    logger.info(f"method={method}-llama3.2:3b, "
                "positive={positive}, "
                "negative={negative}")

    return OkResponse()
