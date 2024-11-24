from typing import Optional, List

from ninja import Schema, Field
from pydantic import Field


class UpdateReportParam(Schema):
    query: str = Field(..., description="查询内容")
    method: str = Field(..., description="方法")
    doc_id: int = Field(..., description="文档ID")
    doc_name: str = Field(..., description="文档名称")
    paragraph_id: int = Field(..., description="段落ID")
    paragraph_title: str = Field(..., description="段落标题")
    paragraph_content: str = Field(..., description="段落内容")
    project_id: str = Field(..., description="所属项目")


class CreateReportParam(Schema):
    reports: List[UpdateReportParam]


class ListReportParam(Schema):
    page: int = Field(1, description="页码")
    # 只能使用默认值，不能被修改
    page_size: int = Field(20, Literal=[20], description="每页数量")
    methods: List[str] = Field(None, description="方法列表")


class MarkReportParam(Schema):
    query: str = Field(..., description="查询内容")
    methods: List[str] = Field(..., description="方法列表")
    paragraph_id: int = Field(..., description="段落ID")
    score: int = Field(..., description="0: 待处理, 1: 有效, -1 无效")
