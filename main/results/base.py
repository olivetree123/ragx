from datetime import datetime

from ninja import Schema


class BaseResult(Schema):
    id: str
    created_at: datetime
    updated_at: datetime
