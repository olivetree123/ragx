# RAGX

RAGX是一个RAG评测系统，收集RAG系统匹配的结果，并对比不同方法的结果的差异

### 构建
```
docker build -t ragx:0.1 .
```

### 运行
```
docker run -d --name=ragx \
    -p 5610:5610 \
    -e DB_HOST="localhost" \
    -e DB_PORT=5432 \
    -e DB_DB="ragx" \
    -e DB_USER="postgres" \
    -e DB_PASSWORD="123456" \
    ragx:0.1
```

### 关于celery
启动命令：
```
celery -A ragx worker --loglevel=info
```
为什么不需要指定 `celery.py` 文件路径呢？

在 Celery 中，-A 选项用于指定 Celery 应用实例的名称，而不是文件路径。Celery 会根据你提供的应用名称自动找到并加载相应的配置。
- 根据 -A ragx，Celery 知道要加载名为 ragx 的应用；
- Celery 会查找 ragx 包，并在其中查找 celery.py 文件；
- Celery 会加载 celery.py 文件中的 Celery 应用实例；

### API
1. 创建项目
```
POST  http://localhost:5610/ragx/project

参数：
{
    "name":"rag01"
}
```
返回值：
```
{
    "id": 1,
    "created_at": "2024-10-02T14:29:25.407226Z",
    "updated_at": "2024-10-02T14:29:25.407226Z",
    "name": "rag01"
}
```

2. 上报匹配的结果
```
POST  http://localhost:5610/ragx/report

参数：
{
    "query":"你好",
    "method":"milvus",
    "project_id": 1,
    "result_ids":[100,101,102],
    "result_contens": ["你好", "你好啊", "你不好"]
}
```
返回值：
```
{
    "id": 3,
    "created_at": "2024-10-02T13:11:34.815647Z",
    "updated_at": "2024-10-02T13:11:34.815647Z",
    "query": "你好",
    "result_ids":[100,101,102],
    "result_contens": ["你好", "你好啊", "你不好"]
    "method": "milvus",
    "project_id": 1
}
```