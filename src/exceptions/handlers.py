from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from .custom_exceptions import CustomException

async def custom_exception_handler(request: Request, exc: CustomException):
    # `exc.status_code`가 None일 경우 기본 상태 코드를 설정
    status_code = exc.status_code if exc.status_code is not None else 500

    return JSONResponse(
        headers={"Access-Control-Allow-Origin": "*"},
        status_code=status_code,
        content={
            "status": status_code,
            "code": exc.error_code.code,
            "message": exc.error_code.message
        },
    )

def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(CustomException, custom_exception_handler)