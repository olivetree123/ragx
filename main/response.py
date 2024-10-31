# from typing import Optional, Any

# from ninja import Schema
from ninja.errors import HttpError

# class OKResponse(Schema):
#     code: Optional[int] = 0
#     data: Optional[Any] = None
#     message: Optional[str] = None

# class FailedResponse(Schema):
#     code: int
#     data: Optional[Any] = None
#     message: Optional[str] = None


class BadRequestError(HttpError):

    def __init__(self, message: str):
        super().__init__(418, message)
