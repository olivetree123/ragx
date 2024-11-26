from typing import List

from django.db.models import (
    CharField,
    TextField,
    IntegerField,
    FloatField,
    SmallIntegerField,
)

from main.models.base import BaseModel
from main.utils.enums import ParagraphStatus


class Report(BaseModel):
    query = CharField(max_length=255, db_comment="查询内容")
    method = CharField(max_length=100, db_comment="使用的方法")
    doc_id = CharField(max_length=32, db_comment="匹配到的文章ID")
    doc_title = CharField(max_length=255, blank=True, db_comment="匹配到的文章标题")
    paragraph_id = CharField(max_length=32, db_comment="匹配到的段落ID")
    paragraph_title = CharField(max_length=255, db_comment="匹配到的段落标题")
    paragraph_content = TextField(db_comment="匹配到的段落内容")
    project_id = CharField(max_length=32, db_comment="所属项目")
    llm_score = SmallIntegerField(
        default=ParagraphStatus.UNKNOWN,
        db_comment=f"大模型打分：{ParagraphStatus.help_text()}")
    human_score = SmallIntegerField(
        default=ParagraphStatus.UNKNOWN,
        db_comment=f"人工打分：{ParagraphStatus.help_text()}")
    rerank_score = FloatField(null=True, default=None, db_comment="重排序得分")

    class Meta:
        db_table = "report"

    @classmethod
    def get_by_query(cls, query: str, methods: List[str], paragraph_id: int,
                     project_id: str):
        return Report.objects.filter(query=query,
                                     method__in=methods,
                                     paragraph_id=paragraph_id,
                                     project_id=project_id).first()
