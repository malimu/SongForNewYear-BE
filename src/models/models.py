from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Song(BaseModel):
    songid: str
    title: str
    artist: str
    category: str
    lyrics: str
    startTime: str
    coverPath: str
    genre: Optional[str]
    youtubePath: str
    blessing: str
    createdAt: datetime
    modifiedAt: datetime

class Wish(BaseModel):
    wishId: str
    nickname: str
    content: str
    isDisplayed: bool = True
    createdAt: datetime
    songid: str
