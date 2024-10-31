from typing import Optional

from pydantic import Field
from ninja import Schema


class CreateProjectParam(Schema):
    name: str = Field(..., max_length=255, description="项目名称")
    description: Optional[str] = Field("", max_length=255, description="项目描述")
