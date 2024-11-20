from datetime import datetime

from ninja import Schema, Field


class BaseResult(Schema):
    id: str
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class Pagination:

    def __init__(self, page: int, size: int):
        self.page = page
        self.size = size

    def paginate(self, queryset):
        return queryset[self.page * self.size:(self.page + 1) * self.size]
