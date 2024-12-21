from .error_codes import ErrorCode

class CustomException(Exception):
    def __init__(self, error_code: ErrorCode):
        self.error_code = error_code
        self.status_code = int(error_code.code[:3])  # 코드의 첫 3자리를 HTTP 상태 코드로 사용