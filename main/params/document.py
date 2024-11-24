from ninja import Schema, Field
from typing import Optional


class CreateDocumentParam(Schema):
    title: str = Field(..., description="文档标题")
    content: str = Field(..., description="文档内容")
    edit_at: str = Field(..., description="文档编辑时间")
