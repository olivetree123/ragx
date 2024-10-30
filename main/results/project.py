from typing import Optional

from main.results.base import BaseResult


class ProjectResult(BaseResult):
    name: str
    description: Optional[str] = ""
