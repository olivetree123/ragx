from typing import Optional, Any

from ninja import Schema


class OKResponse(Schema):
    code: Optional[int] = 0
    data: Optional[Any] = None
    message: Optional[str] = None


class FailedResponse(Schema):
    code: int
    data: Optional[Any] = None
    message: Optional[str] = None
