from typing import List

from main import models


class Paragraph(object):

    @classmethod
    def filter_by_doc_names(cls, names: List[str]):
        documents = models.Document.list_by_names(names=names)
        paragraphs = models.Paragraph.filter_by_document_id_list(
            [doc.id for doc in documents])
        return paragraphs

    @classmethod
    def filter_by_ids(cls, ids: List[int]):
        rs = models.Paragraph.list_by_ids(ids=ids)
