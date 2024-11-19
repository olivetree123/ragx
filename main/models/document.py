from django.db.models import (
    Index,
    CharField,
    TextField,
    BooleanField,
)

from main.models.base import BaseModel


class Document(BaseModel):
    title = CharField(max_length=100, db_comment="文档标题")
    content = TextField(db_comment="文档内容")
    edit_at = CharField(max_length=20, db_comment="编辑时间")
    project_id = CharField(max_length=32, db_comment="所属项目")
    is_paragraphed = BooleanField(default=False, db_comment="是否已经分段")

    class Meta:
        db_table = "document"
        indexes = [Index(fields=["title"]), Index(fields=["edit_at"])]

    @classmethod
    def get_by_title(cls, title, project_id):
        return Document.objects.filter(title=title,
                                       project_id=project_id).first()

    @classmethod
    def list_by_project(cls, project_id):
        return Document.objects.filter(
            project_id=project_id).order_by("-edit_at")

    @classmethod
    def list_unparagraphed(cls):
        return Document.objects.filter(is_paragraphed=False)

    def update(self, title, content, edit_at):
        self.title = title
        self.content = content
        self.edit_at = edit_at
        self.is_paragraphed = False
        self.save()
        return self
