from typing import Optional, List, Literal

from ninja import Schema
from pydantic import Field


class UpdateReportParam(Schema):
    query: str
    method: str
    doc_id: int
    doc_name: str
    paragraph_id: int
    paragraph_title: str
    paragraph_content: str
    project_id: str


class CreateReportParam(Schema):
    reports: List[UpdateReportParam]


class ListReportParam(Schema):
    page: int = 1
    # 只能使用默认值，不能被修改
    page_size: Literal[20] = 20
    methods: Optional[List[str]] = None


class MarkReportParam(Schema):
    query: str
    methods: List[str]
    paragraph_id: int
    project_id: str
    score: int = Field(..., description="0: 待处理, 1: 有效, -1 无效")
