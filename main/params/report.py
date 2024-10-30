from typing import Optional, List

from ninja import Schema


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
