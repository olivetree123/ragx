from datetime import datetime
from typing import List
from ninja import Schema, Field


class DocumentResult(Schema):
    id: str
    title: str = Field(..., description="文档标题")
    content: str = Field(..., description="文档内容")
    edit_at: str = Field(..., description="编辑时间")
    project_id: str = Field(..., description="所属项目")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
