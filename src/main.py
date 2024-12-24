from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.database import init_db
from src.domain.wish.routers import router as wish_router
from src.domain.song.routers import router as song_router
from src.exceptions.handlers import setup_exception_handlers

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

expose_headers = [
    "Authorization",
    "Location"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=expose_headers
)

# 전역 Exception 핸들러 등록
setup_exception_handlers(app)

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(wish_router, prefix="/api/wish", tags=["wish"])
app.include_router(song_router, prefix="/api/song", tags=["song"])