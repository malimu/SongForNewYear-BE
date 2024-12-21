from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 소원 생성 요청 스키마
class WishCreate(BaseModel):
    nickname: str
    content: str
    songid: str

# 소원 응답 스키마
class WishResponse(BaseModel):
    wishid: str
    nickname: str
    content: str
    isDisplayed: bool
    createdAt: datetime
    songid: str

    class Config:
        orm_mode = True
