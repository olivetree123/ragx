# RAGX

RAGX是一个RAG评测系统，收集RAG系统匹配的结果，并对比不同方法的结果的差异

### 运行
```
docker run -d --name=ragx \
    -p 5610:5610 \
    -e MYSQL_HOST="localhost" \
    -e MYSQL_PORT=3306 \
    -e MYSQL_DB="ragx" \
    -e MYSQL_USER="root" \
    -e MYSQL_PASSWORD="123456" \
    ragx:0.1
```

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