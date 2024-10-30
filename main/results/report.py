from main.results.base import BaseResult


class ReportResult(BaseResult):
    query: str
    method: str
    doc_id: int
    doc_name: str
    paragraph_id: int
    paragraph_title: str
    paragraph_content: str
    project_id: str
    match_status: int
