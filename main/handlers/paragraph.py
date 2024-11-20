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


def GetParagraphHandler(request, paragraph_id: str):
    paragraph = models.Paragraph.get_by_id(id=paragraph_id)
    if not paragraph:
        return FailResponse(code=APIStatus.OBJECT_NOT_FOUND)
    return OkResponse(results.ParagraphResult.from_orm(paragraph))


def ListParagraphHandler(request,
                         project_id: str,
                         document_id: Optional[str] = None,
                         page: int = 0,
                         page_size: int = 10):
    if document_id:
        rs = models.Paragraph.objects.filter(document_id=document_id)
    else:
        rs = models.Paragraph.objects.filter(project_id=project_id)
    rs = results.Pagination(page, page_size).paginate(rs)
    return OkResponse(data=[results.ParagraphResult.from_orm(r) for r in rs])
