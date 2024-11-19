from pydantic import Field

from main.results.base import BaseResult


class ReportResult(BaseResult):
    query: str = Field(..., description="查询内容")
    method: str = Field(..., description="方法")
    doc_id: int = Field(..., description="文档ID")
    doc_name: str = Field(..., description="文档名称")
    paragraph_id: int = Field(..., description="段落ID")
    paragraph_title: str = Field(..., description="段落标题")
    paragraph_content: str = Field(..., description="段落内容")
    project_id: str = Field(..., description="所属项目")
    score: int = Field(..., description="0: 待处理, 1: 有效, -1 无效")
