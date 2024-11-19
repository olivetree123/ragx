from django.shortcuts import get_object_or_404
from ninja.pagination import paginate

from main import (
    models,
    params,
    results,
)
from main.tasks import doc_handle, doc_delete


def CreateDocumentHandler(request, param: params.CreateDocumentParam):
    doc = models.Document.get_by_title(title=param.title,
                                       project_id=param.project_id)
    if doc:
        doc.update(**param.model_dump())
        doc_delete(doc.id)
        doc_handle.delay(doc.id, doc.content, doc.project_id)
        return results.DocumentResult.from_orm(doc)
    doc = models.Document.objects.create(**param.model_dump())
    doc_handle.delay(doc.id, doc.content, doc.project_id)
    return results.DocumentResult.from_orm(doc)


def GetDocumentHandler(request, doc_id: str):
    doc = get_object_or_404(models.Document, id=doc_id)
    return results.DocumentResult.from_orm(doc)


@paginate(results.CustomPagination)
def ListDocumentHandler(request, project_id: str):
    return models.Document.list_by_project(project_id=project_id)


def DeleteDocumentHandler(request, doc_id: str):
    doc = get_object_or_404(models.Document, id=doc_id)
    doc.delete()
    doc_delete.delay(doc_id)
    return {"success": True}
