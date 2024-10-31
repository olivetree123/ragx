from typing import (
    Any,
    Dict,
    List,
    Union,
    Optional,
    Callable,
)

from ninja import NinjaAPI, Router
from ninja.security import HttpBearer
from ninja.throttling import BaseThrottle
from ninja.constants import NOT_SET, NOT_SET_TYPE

from main import results
from main.handlers import project, report


class TokenAuth(HttpBearer):

    def authenticate(self, request, token):
        if token == "supersecret":
            return token


class MyRouter(Router):

    def get(self,
            path,
            handler: Callable,
            *,
            auth: Any = NOT_SET,
            throttle: Union[BaseThrottle, List[BaseThrottle],
                            NOT_SET_TYPE] = NOT_SET,
            response: Any = NOT_SET,
            operation_id: Optional[str] = None,
            summary: Optional[str] = None,
            description: Optional[str] = None,
            tags: Optional[List[str]] = None,
            deprecated: Optional[bool] = None,
            by_alias: bool = False,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
            url_name: Optional[str] = None,
            include_in_schema: bool = True,
            openapi_extra: Optional[Dict[str, Any]] = None):
        return super().get(path,
                           auth=auth,
                           throttle=throttle,
                           response=response,
                           operation_id=operation_id,
                           summary=summary,
                           description=description,
                           tags=tags,
                           deprecated=deprecated,
                           by_alias=by_alias,
                           exclude_unset=exclude_unset,
                           exclude_defaults=exclude_defaults,
                           exclude_none=exclude_none,
                           url_name=url_name,
                           include_in_schema=include_in_schema,
                           openapi_extra=openapi_extra)(handler)

    def post(self,
             path,
             handler: Callable,
             *,
             auth: Any = NOT_SET,
             throttle: Union[BaseThrottle, List[BaseThrottle],
                             NOT_SET_TYPE] = NOT_SET,
             response: Any = NOT_SET,
             operation_id: Optional[str] = None,
             summary: Optional[str] = None,
             description: Optional[str] = None,
             tags: Optional[List[str]] = None,
             deprecated: Optional[bool] = None,
             by_alias: bool = False,
             exclude_unset: bool = False,
             exclude_defaults: bool = False,
             exclude_none: bool = False,
             url_name: Optional[str] = None,
             include_in_schema: bool = True,
             openapi_extra: Optional[Dict[str, Any]] = None):
        return super().post(path,
                            auth=auth,
                            throttle=throttle,
                            response=response,
                            operation_id=operation_id,
                            summary=summary,
                            description=description,
                            tags=tags,
                            deprecated=deprecated,
                            by_alias=by_alias,
                            exclude_unset=exclude_unset,
                            exclude_defaults=exclude_defaults,
                            exclude_none=exclude_none,
                            url_name=url_name,
                            include_in_schema=include_in_schema,
                            openapi_extra=openapi_extra)(handler)

    def put(self,
            path,
            handler: Callable,
            *,
            auth: Any = NOT_SET,
            throttle: Union[BaseThrottle, List[BaseThrottle],
                            NOT_SET_TYPE] = NOT_SET,
            response: Any = NOT_SET,
            operation_id: Optional[str] = None,
            summary: Optional[str] = None,
            description: Optional[str] = None,
            tags: Optional[List[str]] = None,
            deprecated: Optional[bool] = None,
            by_alias: bool = False,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
            url_name: Optional[str] = None,
            include_in_schema: bool = True,
            openapi_extra: Optional[Dict[str, Any]] = None):
        return super().put(path,
                           auth=auth,
                           throttle=throttle,
                           response=response,
                           operation_id=operation_id,
                           summary=summary,
                           description=description,
                           tags=tags,
                           deprecated=deprecated,
                           by_alias=by_alias,
                           exclude_unset=exclude_unset,
                           exclude_defaults=exclude_defaults,
                           exclude_none=exclude_none,
                           url_name=url_name,
                           include_in_schema=include_in_schema,
                           openapi_extra=openapi_extra)(handler)

    def delete(self,
               path,
               handler: Callable,
               *,
               auth: Any = NOT_SET,
               throttle: Union[BaseThrottle, List[BaseThrottle],
                               NOT_SET_TYPE] = NOT_SET,
               response: Any = NOT_SET,
               operation_id: Optional[str] = None,
               summary: Optional[str] = None,
               description: Optional[str] = None,
               tags: Optional[List[str]] = None,
               deprecated: Optional[bool] = None,
               by_alias: bool = False,
               exclude_unset: bool = False,
               exclude_defaults: bool = False,
               exclude_none: bool = False,
               url_name: Optional[str] = None,
               include_in_schema: bool = True,
               openapi_extra: Optional[Dict[str, Any]] = None):
        return super().delete(path,
                              auth=auth,
                              throttle=throttle,
                              response=response,
                              operation_id=operation_id,
                              summary=summary,
                              description=description,
                              tags=tags,
                              deprecated=deprecated,
                              by_alias=by_alias,
                              exclude_unset=exclude_unset,
                              exclude_defaults=exclude_defaults,
                              exclude_none=exclude_none,
                              url_name=url_name,
                              include_in_schema=include_in_schema,
                              openapi_extra=openapi_extra)(handler)


# class MyRenderer(JSONRenderer):

#     def render(self, request, data, *, response_status):
#         if not isinstance(data, FailedResponse):
#             data = OKResponse(data=data)
#         return super().render(request, data, response_status=response_status)

api = NinjaAPI(title="RAGX API", version="0.1.0")

project_router = MyRouter(tags=["project"])
report_router = MyRouter(tags=["report"])

api.add_router("project", project_router)
api.add_router("report", report_router)

project_router.post("create",
                    project.CreateProjectHandler,
                    summary="| 创建项目",
                    response=results.ProjectResult)
project_router.get("list",
                   project.ListProjectHandler,
                   summary="| 获取项目列表",
                   response=List[results.ProjectResult])
project_router.get("{project_id}/get",
                   project.GetProjectHandler,
                   summary="| 获取项目详情",
                   response=results.ProjectResult)
project_router.get("{project_id}/update",
                   project.UpdateProjectHandler,
                   summary="| 更新项目信息",
                   response=results.ProjectResult)

report_router.post("create",
                   report.CreateReportHandler,
                   summary="| 创建报告",
                   response=Dict[Any, Any])
report_router.get("list",
                  report.ListReportHandler,
                  summary="| 获取报告列表",
                  response=List[results.ReportResult])
report_router.get("{report_id}/get",
                  report.GetReportHandler,
                  summary="| 获取报告详情",
                  response=results.ReportResult)
report_router.post("{report_id}/update",
                   report.UpdateReportHandler,
                   summary="| 更新报告",
                   response=results.ReportResult)

# urlpatterns = []
