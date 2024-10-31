from main import (
    models,
    params,
    results,
)
from main.response import BadRequestError


def GetProjectHandler(request, project_id: str):
    try:
        project = models.Project.objects.get(id=project_id)
    except models.Project.DoesNotExist:
        raise BadRequestError("Project not found")
    return results.ProjectResult.from_orm(project)


def CreateProjectHandler(request, param: params.CreateProjectParam):
    project = models.Project.objects.create(**param.dict())
    return results.ProjectResult.from_orm(project)


def UpdateProjectHandler(request, project_id: str):
    try:
        project = models.Project.objects.get(id=project_id)
    except models.Project.DoesNotExist:
        raise BadRequestError("Project not found")
    project.update(**request.data)
    return results.ProjectResult.from_orm(project)


def DeleteProjectHandler(request, project_id: str):
    print(f"pretend to delete project where project_id={project_id}")
    return {}


def ListProjectHandler(request):
    projects = models.Project.objects.all()
    rs = [results.ProjectResult.from_orm(p) for p in projects]
    return rs
