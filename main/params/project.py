from typing import Optional

from ninja import Schema


class CreateProjectParam(Schema):
    name: str
    description: Optional[str] = ""
