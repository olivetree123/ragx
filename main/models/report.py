from django.db import models

from main.models.base import BaseModel


class Report(BaseModel):
    query = models.CharField(verbose_name="查询内容", max_length=255)
    doc_ids = models.JSONField(verbose_name="匹配到的文章ID列表", null=True)
    doc_names = models.JSONField(verbose_name="匹配到的文章标题列表", null=True)
    paragraph_ids = models.JSONField(verbose_name="匹配到的段落ID列表")
    paragraph_titles = models.JSONField(verbose_name="匹配到的段落标题列表", null=True)
    paragraph_contents = models.JSONField(verbose_name="匹配到的段落内容列表")
    method = models.CharField(verbose_name="使用的方法", max_length=100)
    project_id = models.IntegerField(verbose_name="所属项目ID")

    class Meta:
        db_table = "report"