from ninja import NinjaAPI

# from . import handlers
from main.handlers import project, report

api = NinjaAPI()
api.post("project/create")(project.CreateProjectHandler)
api.get("project/{project_id}/get")(project.GetProjectHandler)
api.get("project/update")(project.UpdateProjectHandler)
api.get("project/list")(project.ListProjectHandler)

api.post("report/create")(report.CreateReportHandler)
api.post("report/{report_id}/update")(report.UpdateReportHandler)
api.get("report/{report_id}/get")(report.GetReportHandler)
api.get("report/list")(report.ListReportHandler)

urlpatterns = [
    # re_path('projects', views.ProjectListView.as_view()),
    # re_path('project', views.ProjectView.as_view()),
    # re_path('project/(?P<project_id>[0-9]+)', views.ProjectView.as_view()),

    # re_path('reports', views.ReportListView.as_view()),
    # re_path('report', views.ReportView.as_view()),
    # re_path('report', views.ReportView.as_view()),
    # re_path('report/(?P<report_id>[0-9]+)', views.ReportView.as_view()),
    # path("api/", api.urls),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
