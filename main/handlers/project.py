from django.db import IntegrityError

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


def GetProjectHandler(request, project_id: str):
    try:
        project = models.Project.objects.get(id=project_id)
    except models.Project.DoesNotExist:
        return FailResponse(code=APIStatus.BAD_REQUEST)
    return OkResponse(results.ProjectResult.from_orm(project))


def CreateProjectHandler(request, param: params.CreateProjectParam):
    try:
        project = models.Project.objects.create(**param.dict())
    except IntegrityError:
        return FailResponse(code=APIStatus.DUPLICATE_DATA)
    return OkResponse(results.ProjectResult.from_orm(project))


def UpdateProjectHandler(request, project_id: str,
                         param: params.UpdateProjectParam):
    try:
        project = models.Project.objects.get(id=project_id)
    except models.Project.DoesNotExist:
        return FailResponse(code=APIStatus.OBJECT_NOT_FOUND)
    if param.name:
        project.name = param.name
    if param.description:
        project.description = param.description
    project.save()
    return OkResponse(results.ProjectResult.from_orm(project))


def DeleteProjectHandler(request, project_id: str):
    models.Project.objects.filter(id=project_id).delete()
    return OkResponse()


def ListProjectHandler(request):
    projects = models.Project.objects.all()
    rs = [results.ProjectResult.from_orm(p) for p in projects]
    return OkResponse(rs)
