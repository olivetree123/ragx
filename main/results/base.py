import math
from datetime import datetime
from typing import List, Optional

import pydantic
from ninja import Schema, Field
from ninja.pagination import PaginationBase


class BaseResult(Schema):
    id: str
    created_at: datetime
    updated_at: datetime


class CustomPagination(PaginationBase):

    def __init__(self, page_size: Optional[int] = None, **kwargs):
        self.page_size = page_size
        super().__init__(**kwargs)

    class Input(Schema):
        page: Optional[int] = Field(1, description="页码")
        page_size: Optional[int] = Field(20, description="每页数量")

    class Output(Schema):
        model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

        page: int
        total_page: int
        items: List[any]

    def paginate_queryset(self, queryset, pagination: Input, **params):
        page = pagination.page
        page_size = self.page_size or pagination.page_size
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        total_count = queryset.count()
        return {
            "items": list(queryset[start_idx:end_idx]),
            "page": page,
            "total_page": math.ceil(total_count / page_size)
        }
