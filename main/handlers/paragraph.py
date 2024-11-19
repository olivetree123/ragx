from typing import Optional

from django.shortcuts import get_object_or_404
from ninja.pagination import paginate

from main import (
    models,
    params,
    results,
)


def GetParagraphHandler(request, paragraph_id: str):
    paragraph = get_object_or_404(models.Paragraph, id=paragraph_id)
    return results.ParagraphResult.from_orm(paragraph)


@paginate(results.CustomPagination)
def ListParagraphHandler(request,
                         project_id: str,
                         document_id: Optional[str] = None):
    if document_id:
        return models.Paragraph.objects.filter(document_id=document_id)
    return models.Paragraph.objects.filter(project_id=project_id)
