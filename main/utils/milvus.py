from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    utility,
)
from django.conf import settings


class Milvus(object):
    collection = None

    @classmethod
    def init(cls):
        connections.connect(host=settings.MILVUS_HOST,
                            port=settings.MILVUS_PORT,
                            db_name=settings.MILVUS_DB)
        fields = [
            FieldSchema(name="pk",
                        dtype=DataType.INT64,
                        is_primary=True,
                        auto_id=True),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=4096),
            FieldSchema(name="sparse_vector",
                        dtype=DataType.SPARSE_FLOAT_VECTOR),
            FieldSchema(name="dense_vector",
                        dtype=DataType.FLOAT_VECTOR,
                        dim=1024),
            FieldSchema(name="paragraph_id",
                        dtype=DataType.VARCHAR,
                        max_length=32),
            FieldSchema(name="document_id",
                        dtype=DataType.VARCHAR,
                        max_length=32),
        ]
        schema = CollectionSchema(fields=fields, description="ragx collection")
        cls.collection = Collection(name=settings.MILVUS_COLLECTION,
                                    schema=schema)
        cls._init_index()

    @classmethod
    def _init_index(cls):
        # 为了使得向量搜索更加高效，需要给向量字段创建索引
        sparse_index = {
            "index_type": "SPARSE_INVERTED_INDEX",
            "metric_type": "IP"
        }
        cls.collection.create_index("sparse_vector", sparse_index)

        dense_index = {"index_type": "AUTOINDEX", "metric_type": "IP"}
        # dense_index = {"index_type": "IVF_FLAT", "metric_type": "IP"}
        cls.collection.create_index("dense_vector", dense_index)

        # 加载collection，将该collection的索引加载到内存
        cls.collection.load()

    @classmethod
    def drop_collection(cls, collection_name):
        connections.connect(host=settings.MILVUS_HOST,
                            port=settings.MILVUS_PORT,
                            db_name=settings.MILVUS_DB)
        utility.drop_collection(collection_name)
