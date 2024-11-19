from django.db.models import CharField, TextField, BooleanField

from main.models.base import BaseModel


class Paragraph(BaseModel):
    title = CharField(max_length=255, db_comment="段落标题")
    content = TextField(db_comment="段落内容")
    document_id = CharField(max_length=32, db_comment="所属文档")
    project_id = CharField(max_length=32, db_comment="所属项目")
    is_embeddinged = BooleanField(default=False, db_comment="是否已经生成嵌入")

    class Meta:
        db_table = "paragraph"

    @classmethod
    def list_unembeddinged(cls):
        return Paragraph.objects.filter(is_embeddinged=False)

    @classmethod
    def update_embeddinged(cls, paragraph_id):
        return Paragraph.objects.filter(id=paragraph_id).update(
            is_embeddinged=True)
