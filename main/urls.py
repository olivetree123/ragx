from typing import (
    Any,
    Dict,
    List,
    Union,
    Optional,
    Callable,
)

from ninja import Redoc
from ninja import NinjaAPI, Router
from ninja.errors import HttpError
from ninja.security import HttpBearer

from main import results
from main.response import OkResponse
from main.handlers import project, report, document, paragraph


class TokenAuth(HttpBearer):

    def authenticate(self, request, token):
        if token == "supersecret":
            return token


class ProjectIDHeader:

    def __call__(self, request):
        project_id = request.headers.get("x-project-id")
        if not project_id:
            raise HttpError(400, "Missing project_id header")
        request.project_id = project_id
        return project_id


class MyRouter(Router):

    def get(self, path, handler, /, **kwargs):
        return super().get(path, **kwargs)(handler)

    def post(self, path, handler, /, **kwargs):
        return super().post(path, **kwargs)(handler)

    def put(self, path, handler, /, **kwargs):
        return super().put(path, **kwargs)(handler)

    def delete(self, path, handler, /, **kwargs):
        return super().delete(path, **kwargs)(handler)


api = NinjaAPI(title="RAGX API", version="0.1.0")

project_router = MyRouter(tags=["project"])
report_router = MyRouter(tags=["report"], auth=ProjectIDHeader())
document_router = MyRouter(tags=["document"], auth=ProjectIDHeader())
paragraph_router = MyRouter(tags=["paragraph"], auth=ProjectIDHeader())

api.add_router("project", project_router)
api.add_router("report", report_router)
api.add_router("document", document_router)
api.add_router("paragraph", paragraph_router)

project_router.post("create",
                    project.CreateProjectHandler,
                    summary="| 创建项目",
                    response=OkResponse[results.ProjectResult])
project_router.get("list",
                   project.ListProjectHandler,
                   summary="| 获取项目列表",
                   response=OkResponse[List[results.ProjectResult]])
project_router.get("{project_id}/get",
                   project.GetProjectHandler,
                   summary="| 获取项目详情",
                   response=OkResponse[results.ProjectResult])
project_router.post("{project_id}/update",
                    project.UpdateProjectHandler,
                    summary="| 更新项目信息",
                    response=OkResponse[results.ProjectResult])

report_router.get("methods",
                  report.ListReportMethodsHandler,
                  summary="| 获取方法列表",
                  response=OkResponse[List[str]])
report_router.post("create",
                   report.CreateReportHandler,
                   summary="| 创建报告",
                   response=OkResponse[Dict[Any, Any]])
report_router.post("list",
                   report.ListReportHandler,
                   summary="| 获取报告列表",
                   response=OkResponse[list])
report_router.get("{report_id}/get",
                  report.GetReportHandler,
                  summary="| 获取报告详情",
                  response=OkResponse[results.ReportResult])
report_router.post("{report_id}/update",
                   report.UpdateReportHandler,
                   summary="| 更新报告",
                   response=OkResponse[results.ReportResult])
report_router.post("mark",
                   report.MarkReportHandler,
                   summary="| 给报告打分",
                   response=OkResponse[results.ReportResult])

document_router.post("",
                     document.CreateDocumentHandler,
                     summary="| 创建文档",
                     response=OkResponse[results.DocumentResult])
document_router.get("list",
                    document.ListDocumentHandler,
                    summary="| 获取文档列表",
                    response=OkResponse[List[results.DocumentResult]])
document_router.get("{doc_id}",
                    document.GetDocumentHandler,
                    summary="| 获取文档详情",
                    response=OkResponse[results.DocumentResult])
document_router.delete("{doc_id}",
                       document.DeleteDocumentHandler,
                       summary="| 删除文档",
                       response=OkResponse[None])

paragraph_router.get("list",
                     paragraph.ListParagraphHandler,
                     summary="| 获取段落列表",
                     response=OkResponse[List[results.ParagraphResult]])
paragraph_router.get("{paragraph_id}",
                     paragraph.GetParagraphHandler,
                     summary="| 获取段落详情",
                     response=OkResponse[results.ParagraphResult])
# urlpatterns = []
