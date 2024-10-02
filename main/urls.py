from django.urls import re_path
# from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    re_path('projects', views.ProjectListView.as_view()),
    re_path('project', views.ProjectView.as_view()),
    re_path('project/(?P<project_id>[0-9]+)', views.ProjectView.as_view()),

    re_path('reports', views.ReportListView.as_view()),
    re_path('report', views.ReportView.as_view()),
    re_path('report/(?P<report_id>[0-9]+)', views.ReportView.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
