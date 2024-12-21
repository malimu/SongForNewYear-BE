from pydantic import Field
from typing import Optional, List
from datetime import datetime

class Song():
    song_index: int
    title: str
    artist: str
    category: str
    lyrics: str
    start_time: str
    cover_path: str
    genre: Optional[str]
    youtube_path: str
    blessing: str
    created_at: datetime
    modified_at: datetime

class Wish():
    wish_id: str
    nickname: str
    content: str
    is_displayed: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)  # 자동 생성 시각 기록
    song_id: str
