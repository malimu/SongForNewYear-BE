from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 노래 생성 요청 스키마
class SongCreate(BaseModel):
    title: str
    artist: str
    category: str
    lyrics: str
    startTime: str
    coverPath: Optional[str] = None
    genre: Optional[str] = None
    youtubePath: str
    blessing: str

# 노래 응답 스키마
class SongResponse(BaseModel):
    songid: str
    title: str
    artist: str
    category: str
    lyrics: str
    startTime: str
    coverPath: Optional[str] = None
    genre: Optional[str] = None
    youtubePath: str
    blessing: str
    createdAt: datetime
    modifiedAt: datetime

    class Config:
        orm_mode = True
