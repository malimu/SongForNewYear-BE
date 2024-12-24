from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 소원 생성 요청 스키마
class WishCreate(BaseModel):
    nickname: str
    content: str
    is_displayed: bool = Field(alias="is_displayed")

# 랜덤4개 소원 응답 스키마
class WishResponse(BaseModel):
    wishid: str = Field(alias="wishId")
    nickname: str
    content: str
    is_displayed: bool = Field(alias="is_displayed")
    created_at: datetime = Field(alias="created_at")
    song_id: str

    class Config:
        from_attributes = True 
        allow_population_by_field_name = True

# 추천 결과 스키마
class SongRecommendation(BaseModel):
    title: str
    artist: str
    lyrics: str
    cover_path: str = Field(alias="cover_path")
    youtube_path: str = Field(alias="youtube_path")
    recommend_time: str = Field(alias="recommend_time")

class RecommendationResponse(BaseModel):
    nickname: str
    wish: str
    recommended_song: SongRecommendation
    wish_id: str = Field(alias="_id")

    class Config:
        from_attributes = True
        allow_population_by_field_name = True