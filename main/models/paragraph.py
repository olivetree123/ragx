from typing import List

from django.db.models import (
    CharField,
    TextField,
    BooleanField,
    ForeignKey,
    CASCADE,
)

from main.models.base import BaseModel
from main.models.document import Document


class Paragraph(BaseModel):
    title = CharField(max_length=255, db_comment="段落标题")
    content = TextField(db_comment="段落内容")
    # document_id = CharField(max_length=32, db_comment="所属文档")
    document = ForeignKey(Document,
                          to_field="id",
                          db_column="document_id",
                          db_comment="所属文档",
                          related_name="paragraphs",
                          default=None,
                          null=False,
                          on_delete=CASCADE)
    project_id = CharField(max_length=32, db_comment="所属项目")
    is_embeddinged = BooleanField(default=False, db_comment="是否已经生成嵌入")

    class Meta:
        db_table = "paragraph"

    @classmethod
    def get_by_id(cls, id, project_id):
        return cls.objects.filter(id=id, project_id=project_id).first()

    @classmethod
    def list_by_ids(cls, ids: List[str], project_id):
        return cls.objects.filter(id__in=ids, project_id=project_id)

    @classmethod
    def list_unembeddinged(cls):
        return Paragraph.objects.filter(is_embeddinged=False)

    @classmethod
    def update_embeddinged(cls, paragraph_id):
        return Paragraph.objects.filter(id=paragraph_id).update(
            is_embeddinged=True)

    @classmethod
    def filter_by_document_ids(cls, document_ids: List[str], project_id):
        return Paragraph.objects.filter(document_id__in=document_ids,
                                        project_id=project_id)
