from django.db import models

from main.models.base import BaseModel


class Report2(BaseModel):
    query = models.CharField(verbose_name="查询内容", max_length=255)
    doc_id = models.IntegerField(verbose_name="匹配到的文章ID")
    doc_name = models.CharField(verbose_name="匹配到的文章标题", max_length=255, blank=True)
    paragraph_id = models.IntegerField(verbose_name="匹配到的段落ID")
    paragraph_title = models.CharField(verbose_name="匹配到的段落标题", max_length=255)
    paragraph_content = models.TextField(verbose_name="匹配到的段落内容")
    method = models.CharField(verbose_name="使用的方法", max_length=100)
    project_id = models.IntegerField(verbose_name="所属项目ID")

    class Meta:
        db_table = "report2"