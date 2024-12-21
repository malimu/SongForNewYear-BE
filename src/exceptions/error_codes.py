from enum import Enum

class ErrorCode(Enum):
    # 4xx 클라이언트 에러
    VALIDATION_ERROR = ("E4001", "Validation error")
    NOT_FOUND = ("E4002", "Resource not found")
    UNAUTHORIZED = ("E4003", "Unauthorized access")
    BAD_REQUEST = ("E4004", "Bad request")

    # 5xx 서버 에러
    INTERNAL_SERVER_ERROR = ("E5001", "Internal server error")
    SERVICE_UNAVAILABLE = ("E5002", "Service unavailable")

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
