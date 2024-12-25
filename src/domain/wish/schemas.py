from pydantic import BaseModel
from datetime import datetime

# 소원 생성 요청 스키마
class WishCreate(BaseModel):
    nickname: str
    content: str
    is_displayed: bool

# 랜덤4개 소원 응답 스키마
class WishRandomResponse(BaseModel):
    nickname: str
    content: str
    is_displayed: bool
    created_at: datetime
    category: str

    class Config:
        from_attributes = True 

# 추천 결과 스키마
class SongRecommendation(BaseModel):
    title: str
    artist: str
    lyrics: str
    cover_path: str
    youtube_path: str
    recommend_time: str 

class RecommendationResponse(BaseModel):
    wish_id: str
    nickname: str
    wish: str
    category: str
    recommended_song: SongRecommendation

    class Config:
        from_attributes = True