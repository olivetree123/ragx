from django.db import models

from main.models.base import BaseModel


class Report(BaseModel):
    query = models.CharField(verbose_name="查询内容", max_length=255)
    result_ids = models.JSONField(verbose_name="匹配到的段落ID列表")
    result_contents = models.JSONField(verbose_name="匹配到的段落内容列表")
    method = models.CharField(verbose_name="使用的方法", max_length=100)
    project_id = models.IntegerField(verbose_name="所属项目ID")

    class Meta:
        db_table = "report"