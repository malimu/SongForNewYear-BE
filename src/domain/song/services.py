from src.domain.song.crud import insert, get_many
from datetime import datetime
from typing import List

# 노래 생성
async def create_song(song_data: dict) -> str:
    song_data["createdAt"] = datetime.now()
    song_data["modifiedAt"] = datetime.now()
    return await insert("songs", song_data)

# 카테고리별 노래 목록 가져오기
async def get_songs_by_category(category: str, skip: int, limit: int) -> List[dict]:
    return await get_many("songs", {"category": category}, skip, limit)

# 노래 검색 (페이징)
async def search_songs(query: str, skip: int, limit: int) -> List[dict]:
    return await get_many("songs", {"title": {"$regex": query, "$options": "i"}}, skip, limit)
