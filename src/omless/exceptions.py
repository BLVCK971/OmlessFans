from typing import List, Optional
from fastapi import HTTPException
from pydantic import BaseModel


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