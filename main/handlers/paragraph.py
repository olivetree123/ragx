from typing import Optional

from main import (
    models,
    params,
    results,
)
from main.response import (
    OkResponse,
    FailResponse,
    APIStatus,
)
from main.md.current import current_project


def GetParagraphHandler(request, paragraph_id: str):
    paragraph = models.Paragraph.get_by_id(id=paragraph_id,
                                           project_id=current_project())
    if not paragraph:
        return FailResponse(code=APIStatus.OBJECT_NOT_FOUND, message="段落不存在")
    return OkResponse(results.ParagraphResult.from_orm(paragraph))


def ListParagraphHandler(request,
                         document_id: Optional[str] = None,
                         page: int = 0,
                         page_size: int = 10):
    if document_id:
        rs = models.Paragraph.objects.filter(document_id=document_id)
    else:
        rs = models.Paragraph.objects.filter(project_id=current_project())
    rs = results.Pagination(page, page_size).paginate(rs)
    return OkResponse(data=[results.ParagraphResult.from_orm(r) for r in rs])
