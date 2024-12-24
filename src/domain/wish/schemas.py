from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 소원 생성 요청 스키마
class WishCreate(BaseModel):
    nickname: str
    content: str
    is_displayed: bool = Field(alias="isDisplayed")

# 랜덤4개 소원 응답 스키마
class WishResponse(BaseModel):
    wishid: str = Field(alias="wishId")
    nickname: str
    content: str
    is_displayed: bool = Field(alias="isDisplayed")
    created_at: datetime = Field(alias="createdAt")
    songid: str

    class Config:
        from_attributes = True 
        allow_population_by_field_name = True

# 추천 결과 스키마
class SongRecommendation(BaseModel):
    title: str
    artist: str
    lyrics: str
    cover_path: str = Field(alias="coverPath")
    youtube_path: str = Field(alias="youtubePath")
    recommend_time: str = Field(alias="recommendtime")

class RecommendationResponse(BaseModel):
    nickname: str
    wish: str
    recommended_song: SongRecommendation
    wish_id: str = Field(alias="wishId")

    class Config:
        from_attributes = True
        allow_population_by_field_name = True