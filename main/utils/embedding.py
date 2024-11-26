from milvus_model.hybrid import BGEM3EmbeddingFunction


# 如果需要使用，需要在程序启动时初始化
class EmbeddingFunction(object):
    _func = None

    @classmethod
    def init(cls):
        cls._func = BGEM3EmbeddingFunction(
            use_fp16=False,
            model_name=
            "E:/mounts/models/models--BAAI--bge-m3/snapshots/5617a9f61b028005a4858fdac845db406aefb181"
        )

    @classmethod
    def call(cls, *args, **kwargs):
        if not cls._func:
            cls.init()
        return cls._func(*args, **kwargs)
