from elasticsearch import Elasticsearch
from django.conf import settings

client = Elasticsearch(hosts=settings.ES_BASE_URL)
result = client.indices.create(index=settings.ES_INDEX_NAME, ignore=400)


def es_save(data: dict):
    client.index(index=settings.ES_INDEX_NAME, id=data["id"], body=data)


def es_search(query: str, limit=20):
    dsl = {"query": {"match": {"title": query}}, "_source": ["title"]}
    result = client.search(index=settings.ES_INDEX_NAME, body=dsl, size=limit)
    docs = []
    for hit in result["hits"]["hits"]:
        docs.append(hit["_source"]["title"])
    return docs


if __name__ == "__main__":
    docs = es_search("杭州才悦云筑人才租赁房有什么信息")
    print(docs)
