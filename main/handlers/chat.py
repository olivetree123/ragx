from typing import Optional

from pymilvus import (
    AnnSearchRequest,
    WeightedRanker,
    RRFRanker,
    SearchResult,
    Hits,
)
from ninja import Schema, Field

from main import (
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


# 发送消息请求模型
class SendMessageRequest(Schema):
    session_id: int
    content: str


def ChatV1Handler(request, message: SendMessageRequest):
    # 1. ES关键字查询
    titles = es_search(message.content)
    names = [title + ".md" for title in titles]
    documents = models.Document.list_by_names(names=names)
    paragraphs = models.Paragraph.filter_by_document_id_list(
        [doc.id for doc in documents])
    paragraph_id_list = [p.id for p in paragraphs]
    # print("es hits = ", paragraph_id_list)

    # 2. 从向量数据库查询
    query_embeddings = EmbeddingFunction.call([message.content])
    query_dense_embedding = query_embeddings["dense"][0]
    query_sparse_embedding = query_embeddings["sparse"]

    sparse_weight = dense_weight = 1.0
    dense_search_params = {"metric_type": "IP", "params": {}}
    dense_req = AnnSearchRequest([query_dense_embedding],
                                 "dense_vector",
                                 dense_search_params,
                                 limit=40)
    sparse_search_params = {"metric_type": "IP", "params": {}}
    sparse_req = AnnSearchRequest([query_sparse_embedding],
                                  "sparse_vector",
                                  sparse_search_params,
                                  limit=40)
    # rerank = WeightedRanker(sparse_weight, dense_weight)
    rerank = RRFRanker()
    hits: Hits = Milvus.collection.hybrid_search(
        [sparse_req, dense_req],
        rerank=rerank,
        limit=40,
        output_fields=["text", "document_id", "paragraph_id"])[0]

    # hits = vector_store.search(query=message.content,
    #                             search_type="similarity",
    #                             k=10)
    # paragraph_id_list += [hit.metadata["paragraph_id"] for hit in hits]
    # print("milvus hits = ", [hit.get("paragraph_id") for hit in hits])

    # 3. 组合查询结果
    paragraph_id_list += [hit.get("paragraph_id") for hit in hits]
    # print("total hits = ", list(set(paragraph_id_list)))
    paragraphs = models.Paragraph.filter_by_id_list(
        paragraph_id_list=paragraph_id_list)

    paragraphs = [{
        "id": p.id,
        "title": p.title,
        "content": p.content,
        "doc_id": p.document_id
    } for p in paragraphs]

    report = [{
        "query": message.content,
        "method": "Milvus-ES-Rerank",
        "paragraph_id": p["id"],
        "paragraph_title": p["title"],
        "paragraph_content": p["content"],
        "doc_id": p["doc_id"],
        "doc_name": "",
        "project_id": current_project(),
    } for p in paragraphs]

    result_paragraph_titles = [p["title"] for p in paragraphs]
    # result_paragraph_contents = [p["content"] for p in paragraphs]

    # 重排序方式1：按段落标题和内容重排序
    # rerank_data = [
    #     result_paragraph_titles[i] + " " + result_paragraph_contents[i]
    #     for i in range(len(result_paragraph_titles))
    # ]

    # 重排序方式2：按段落标题重排序
    # 4. 重排序
    scores = rerank_service(message.content, result_paragraph_titles)

    for i, score in enumerate(scores):
        if score < -0.5:
            report[i] = None
            # result_paragraph_contents[i] = ""

    report = [item for item in report if item]
    # result_paragraph_contents = [
    #     item for item in result_paragraph_contents if item
    # ]

    # 5. 上报到ragx
    try:
        ragx.add_report(data=report)
    except:
        import traceback
        traceback.print_exc()

    # TODO: 测试中，暂时不记住聊天历史
    # chat_history = get_history(session=session, scene_id=message.scene_id)
    # chat_history = []
    # current_msg = HumanMessage(question=message.content,
    #                            paragraph_list=result_paragraph_contents)
    # chat_history.append(current_msg.json())
    # response_content = together_chat(messages=chat_history)
    # print("response_content=", response_content)
    # models.Message.send_to_assitant(session=session,
    #                                 scene_id=message.scene_id,
    #                                 sender_role=MessageRole.USER,
    #                                 sender_user=current_user.id,
    #                                 paragraph_list=paragraph_id_list,
    #                                 content=message.content)
    # models.Message.send_to_user(session=session,
    #                             scene_id=message.scene_id,
    #                             sender_role=MessageRole.ASSISTANT,
    #                             recipient_user=current_user.id,
    #                             content=response_content)
    return {
        "status": 1,
        "error": "",
        "data": "",
    }
