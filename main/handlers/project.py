from main import (
    models,
    params,
    results,
)
from main.response import OKResponse, FailedResponse


def GetProjectHandler(request, project_id: str):
    try:
        project = models.Project.objects.get(id=project_id)
    except models.Project.DoesNotExist:
        return FailedResponse(code=400, message="Project not found")
    r = results.ProjectResult.from_orm(project)
    return OKResponse(data=r)


def CreateProjectHandler(request, param: params.CreateProjectParam):
    project = models.Project.objects.create(**param.dict())
    r = results.ProjectResult.from_orm(project)
    return OKResponse(data=r)


def UpdateProjectHandler(request, project_id: str):
    try:
        project = models.Project.objects.get(id=project_id)
    except models.Project.DoesNotExist:
        return FailedResponse(code=400, message="Project not found")
    project.update(**request.data)
    r = results.ProjectResult.from_orm(project)
    return OKResponse(result=r)


def DeleteProjectHandler(request, project_id: str):
    print(f"pretend to delete project where project_id={project_id}")
    return OKResponse()


def ListProjectHandler(request):
    projects = models.Project.objects.all()
    rs = [results.ProjectResult.from_orm(p) for p in projects]
    return OKResponse(data=rs)
