from pymilvus import (
    Hits,
    RRFRanker,
    SearchResult,
    WeightedRanker,
    AnnSearchRequest,
)

from main.utils.milvus import MilvusClient
from main.utils.embedding import EmbeddingFunction


class Milvus(object):

    @classmethod
    def hybrid_search(cls, text: str, limit=40):
        query_embeddings = EmbeddingFunction.call([text])
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
        hits: Hits = MilvusClient.collection.hybrid_search(
            [sparse_req, dense_req],
            rerank=rerank,
            limit=40,
            output_fields=["text", "document_id", "paragraph_id"])[0]
        return hits
