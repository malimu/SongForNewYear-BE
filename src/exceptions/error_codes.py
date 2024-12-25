from enum import Enum

class ErrorCode(Enum):
    # 4xx 클라이언트 에러
    INVALID_INPUT_FORMAT = ("4001", "유효하지 않은 형식입니다.")
    INVALID_INPUT_VALUE = ("4002", "입력값이 잘못되었습니다.")
    MISSING_PARAMETER = ("4003", "필수 파라미터가 누락되었습니다.")
    USER_NOT_FOUND = ("4041", "사용자를 찾을 수 없습니다.")
    SONG_NOT_FOUND = ("4042", "노래를 찾을 수 없습니다.")
    WISH_NOT_FOUND = ("4043", "요청한 소원을 찾을 수 없습니다.")
    UNAUTHORIZED_ACCESS = ("4011", "권한이 없습니다.")
    DUPLICATE_ENTRY = ("4091", "중복된 항목이 존재합니다.")

    # 5xx 서버 에러
    INTERNAL_SERVER_ERROR = ("5001", "서버 내부 오류가 발생했습니다.")
    EXTERNAL_SERVICE_ERROR = ("5002", "외부 서비스 호출 중 오류가 발생했습니다.")
    
    SONG_CATEGORY_IS_MISSING = ("5003", "노래에 카테고리가 누락되었습니다.")

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message

    def to_dict(self):
        return {"code": self.code, "message": self.message}