from fastapi import HTTPException
from .error_codes import ErrorCode

class CustomException(HTTPException):
    def __init__(self, error_code: ErrorCode, status_code: int = 400, detail: str = None):
        self.error_code = error_code
        self.status_code = status_code
        self.detail = detail or error_code.message
        super().__init__(
            status_code=status_code,
            detail={"code": error_code.code, "message": self.detail},
        )
