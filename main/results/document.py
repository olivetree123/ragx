from datetime import datetime
from typing import List
from ninja import Schema


class DocumentResult(Schema):
    id: str
    title: str
    content: str
    edit_at: str
    project_id: str
    created_at: datetime
    updated_at: datetime
