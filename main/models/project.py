from django.db.models import CharField

from main.models.base import BaseModel


class Project(BaseModel):
    name = CharField(db_comment="项目名称", max_length=100)
    description = CharField(max_length=255,
                            null=True,
                            blank=True,
                            db_comment="项目描述")

    class Meta:
        db_table = "project"
