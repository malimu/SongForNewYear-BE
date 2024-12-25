from pydantic import BaseModel, Field
from datetime import datetime

# 소원 생성 요청 스키마
class WishCreate(BaseModel):
    nickname: str
    content: str
    is_displayed: bool

# 랜덤 4개 소원 응답 스키마
class WishRandomResponse(BaseModel):
    nickname: str
    content: str
    is_displayed: bool
    created_at: datetime
    category: str

    class Config:
        from_attributes = True 
        allow_population_by_field_name = True

# 추천 결과 스키마
class SongRecommendation(BaseModel):
    title: str
    artist: str
    lyrics: str
    cover_path: str
    youtube_path: str
    recommend_time: str = Field(alias="recommend_time")

class RecommendationResponse(BaseModel):
    wish_id: str
    nickname: str
    wish: str
    category: str
    recommended_song: SongRecommendation
    wishes_count: int

    class Config:
        from_attributes = True
        allow_population_by_field_name = True