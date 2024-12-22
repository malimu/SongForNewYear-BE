from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# 노래 응답 스키마
class SongUnitResponse(BaseModel):
    title: str
    artist: str
    category: str
    lyrics: str
    coverPath: Optional[str] = None
    youtubePath: str

    class Config:
        orm_mode = True

# 페이지네이션 응답 스키마
class PaginatedResponse(BaseModel):
    total_pages: int
    current_page: int
    page_size: int
    total_items: int
    data: List[SongUnitResponse]