from src.core.crud import get_many, get_by_id, count_by_column
from typing import List

# 카테고리별 노래 목록 가져오기
async def get_songs_by_category(category: str, skip: int, limit: int) -> List[dict]:
    return await get_many("songs", {"category": category}, skip, limit)

# 카테고리에 맞는 총 노래 수를 반환
async def get_total_songs_count(category: str) -> int:
    count = await count_by_column("songs", "category", category)
    return count

# obj_id로 노래 가져오기
async def get_song_by_obj_id(obj_id: object):
    return await get_by_id("songs", obj_id)


'''
# 노래 생성
async def create_song(song_data: dict) -> str:
    song_data["createdAt"] = datetime.now()
    song_data["modifiedAt"] = datetime.now()
    return await insert("songs", song_data)
    
# 노래 검색 (페이징)
async def search_songs(query: str, skip: int, limit: int) -> List[dict]:
    return await get_many("songs", {"title": {"$regex": query, "$options": "i"}}, skip, limit)
'''