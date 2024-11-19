from datetime import datetime
from typing import List
from ninja import Schema
from pydantic import Field


class ParagraphResult(Schema):
    id: str = Field(..., description="段落的唯一标识符")
    title: str = Field(..., description="段落标题")
    content: str = Field(..., description="段落内容")
    document_id: str = Field(..., description="所属文档")
    project_id: str = Field(..., description="所属项目")
    is_embeddinged: bool = Field(..., description="是否已生成向量")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
