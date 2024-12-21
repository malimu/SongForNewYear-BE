from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from .custom_exceptions import CustomException

async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code.code,
                "message": exc.detail,
            },
        },
    )

def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(CustomException, custom_exception_handler)
