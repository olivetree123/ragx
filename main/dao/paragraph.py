from typing import List

from main import models


class Paragraph(object):

    @classmethod
    def filter_by_doc_names(cls, names: List[str], project_id: str):
        documents = models.Document.list_by_names(names=names)
        paragraphs = models.Paragraph.filter_by_document_ids(
            [doc.id for doc in documents], project_id=project_id)
        return paragraphs

    @classmethod
    def filter_by_ids(cls, ids: List[int]):
        # models.Paragraph 和  models.Document 连表查询
        rs = models.Paragraph.list_by_ids(ids=ids)
