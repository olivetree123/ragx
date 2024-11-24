import re

from ninja import File
from ninja.files import UploadedFile

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
from main.utils.log import get_logger
from main.md.current import current_project

logger = get_logger(name="handlers.document")


def CreateDocumentHandler(request, param: params.CreateDocumentParam):
    doc = models.Document.get_by_title(title=param.title,
                                       project_id=current_project())
    if doc:
        doc.update(**param.model_dump())
        doc_delete(doc.id)
        doc_handle.delay(doc.id, doc.content, doc.project_id)
        return OkResponse(results.DocumentResult.from_orm(doc))
    doc = models.Document.objects.create(**param.model_dump(),
                                         project_id=current_project())
    doc_handle.delay(doc.id, doc.content, doc.project_id)
    return OkResponse(data=results.DocumentResult.from_orm(doc))


def GetDocumentHandler(request, doc_id: str):
    doc = models.Document.get_by_id(id=doc_id)
    if not doc:
        return FailResponse(code=APIStatus.OBJECT_NOT_FOUND)
    return OkResponse(results.DocumentResult.from_orm(doc))


def ListDocumentHandler(request, page: int = 0, page_size: int = 10):
    rs = models.Document.list_by_project(project_id=current_project())
    rs = results.Pagination(page, page_size).paginate(rs)
    return OkResponse(data=[results.DocumentResult.from_orm(r) for r in rs])


def DeleteDocumentHandler(request, doc_id: str):
    doc = models.Document.get_by_id(id=doc_id)
    if not doc:
        return FailResponse(code=APIStatus.OBJECT_NOT_FOUND)
    doc.delete()
    doc_delete.delay(doc_id)
    return OkResponse()


# def UploadDocumentHandler(request,
#                           project_id: str,
#                           file: UploadedFile = File(...)):
#     body = str(file.read(), encoding="utf8").strip()
#     # 使用正则表达式匹配每个一级标题及其后面的内容
#     pattern = re.compile(r"(^# .+?)(?=^# |\Z)", re.MULTILINE | re.DOTALL)
#     matches = pattern.findall(body)

#     for match in matches:
#         # 分离标题和内容
#         lines = match.split("\n", 1)
#         title = lines[0].strip()
#         content = lines[1].strip() if len(lines) > 1 else ""
#         if not title:
#             logger.error("Empty title")
#             continue
#         # TODO: 缺少edit_at字段
#         doc = models.Document.objects.create(title=title,
#                                              content=content,
#                                              project_id=project_id)
#         doc_handle(doc.id, doc.content, doc.project_id)
#     return OkResponse(data={"name": file.name})
