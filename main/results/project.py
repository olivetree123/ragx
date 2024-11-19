from typing import Optional

from pydantic import Field

from main.results.base import BaseResult


class ProjectResult(BaseResult):
    """项目详情"""
    name: str = Field(..., description="项目名称")
    description: Optional[str] = Field("", description="项目描述")
