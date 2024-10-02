from django.db import models

from main.models.base import BaseModel


class Project(BaseModel):
    name = models.CharField(verbose_name="项目名称", max_length=100)

    class Meta:
        db_table = "project"