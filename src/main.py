from fastapi import FastAPI
from src.core.database import init_db
from src.domain.wish.routers import router as wish_router
from src.domain.wish.routers import router as wish_router
from src.domain.song.routers import router as song_router

from src.exceptions.handlers import setup_exception_handlers

app = FastAPI()

# 전역 Exception 핸들러 등록
setup_exception_handlers(app)


@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(wish_router, prefix="/api/wish", tags=["Wish"])
app.include_router(song_router, prefix="/api/song", tags=["Song"])