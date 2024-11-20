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
from main.tasks import doc_handle, doc_delete


def CreateDocumentHandler(request, param: params.CreateDocumentParam):
    doc = models.Document.get_by_title(title=param.title,
                                       project_id=param.project_id)
    if doc:
        doc.update(**param.model_dump())
        doc_delete(doc.id)
        doc_handle.delay(doc.id, doc.content, doc.project_id)
        return OkResponse(results.DocumentResult.from_orm(doc))
    doc = models.Document.objects.create(**param.model_dump())
    doc_handle.delay(doc.id, doc.content, doc.project_id)
    return OkResponse(data=results.DocumentResult.from_orm(doc))


def GetDocumentHandler(request, doc_id: str):
    doc = models.Document.get_by_id(id=doc_id)
    if not doc:
        return FailResponse(code=APIStatus.OBJECT_NOT_FOUND)
    return OkResponse(results.DocumentResult.from_orm(doc))


def ListDocumentHandler(request,
                        project_id: str,
                        page: int = 0,
                        page_size: int = 10):
    rs = models.Document.list_by_project(project_id=project_id)
    rs = results.Pagination(page, page_size).paginate(rs)
    return OkResponse(data=[results.DocumentResult.from_orm(r) for r in rs])


def DeleteDocumentHandler(request, doc_id: str):
    doc = models.Document.get_by_id(id=doc_id)
    if not doc:
        return FailResponse(code=APIStatus.OBJECT_NOT_FOUND)
    doc.delete()
    doc_delete.delay(doc_id)
    return OkResponse()
