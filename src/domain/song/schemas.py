from pydantic import Field, BaseModel
from typing import List, Optional

# 노래 응답 스키마
class SongUnitResponse(BaseModel):
    title: str
    artist: str
    category: str
    lyrics: str
    cover_path: Optional[str] = None
    youtube_path: Optional[str] = None
    start_time: str = Field(alias="start_time")
    total_time: str = Field(alias="total_time")

    class Config:
        orm_mode = True

# 페이지네이션 응답 스키마
class PaginatedResponse(BaseModel):
    total_pages: int
    current_page: int
    page_size: int
    total_items: int
    data: List[SongUnitResponse]