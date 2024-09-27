from typing import List, Optional
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic.errors import PydanticValueError

class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMessage]]


class RateLimitExceeded(HTTPException):
    """
    exception raised when a rate limit is hit.
    """

    limit = None

    def __init__(self, limit: Limit) -> None:
        self.limit = limit
        if limit.error_message:
            description: str = (
                limit.error_message
                if not callable(limit.error_message)
                else limit.error_message()
            )
        else:
            description = str(limit.limit)
        super(RateLimitExceeded, self).__init__(status_code=429, detail=description)


class DispatchException(Exception):
    pass


class DispatchPluginException(DispatchException):
    pass


class NotFoundError(PydanticValueError):
    code = "not_found"
    msg_template = "{msg}"


class FieldNotFoundError(PydanticValueError):
    code = "not_found.field"
    msg_template = "{msg}"


class ModelNotFoundError(PydanticValueError):
    code = "not_found.model"
    msg_template = "{msg}"


class ExistsError(PydanticValueError):
    code = "exists"
    msg_template = "{msg}"


class InvalidConfigurationError(PydanticValueError):
    code = "invalid.configuration"
    msg_template = "{msg}"


class InvalidFilterError(PydanticValueError):
    code = "invalid.filter"
    msg_template = "{msg}"


class InvalidUsernameError(PydanticValueError):
    code = "invalid.username"
    msg_template = "{msg}"


class InvalidPasswordError(PydanticValueError):
    code = "invalid.password"
    msg_template = "{msg}"