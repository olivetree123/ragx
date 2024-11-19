from ninja.errors import HttpError


class BadRequestError(HttpError):

    def __init__(self, message: str):
        super().__init__(418, message)
