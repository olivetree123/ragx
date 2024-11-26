from typing import List

import requests
from django.conf import settings
from FlagEmbedding import FlagReranker

reranker = FlagReranker("BAAI/bge-reranker-v2-m3",
                        use_fp16=False,
                        cache_dir="./")


def rerank(query: str, data: List[str]):
    if not isinstance(data, (list, tuple)):
        raise TypeError("`data` must be a list or tuple")
    data = [[query, d] for d in data]
    return reranker.compute_score(data)


def rerank_service(query, data: List[str]):
    """调用重排序模型的接口，返回分数列表"""
    url = f"{settings.RERANKER_BASE_URL}/rerank"
    r = requests.post(url, json={"query": query, "data": data})
    if not r.ok:
        raise requests.HTTPError("Failed to request reranker service",
                                 response=r)
    resp = r.json()
    if resp["code"] != 0:
        raise requests.HTTPError(
            "Failed to request reranker service, code={}, message={}".format(
                resp["code"], resp["message"]))
    return resp["data"]
