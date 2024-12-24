from src.core.database import db
from src.core.crud import get_many, get_by_id, count_by_column
from typing import Optional, List

# 카테고리별 노래 목록 가져오기
async def get_songs_by_category(category: Optional[str], skip: int, limit: int) -> List[dict]:
    # category가 None이면 전체 데이터를 가져오도록 필터를 빈 딕셔너리로 설정
    filter_query = {"category": category} if category else {}
    return await get_many("song", filter_query, skip, limit)

# 카테고리에 맞는 총 노래 수를 반환
async def get_total_songs_count(category: str) -> int:
    count = await count_by_column("song", "category", category)
    return count

# _id로 노래 가져오기
async def get_song_by_obj_id(_id: object):
    return await get_by_id("song", _id)

# 특정 카테고리에서 랜덤으로 한 곡을 선택
async def get_random_song_by_category(category: str) -> dict:
    songs = await db["song"].aggregate([
        {"$match": {"category": category}},
        {"$sample": {"size": 1}}  
    ]).to_list(length=1)
    return songs[0]


'''
# 노래 생성
async def create_song(song_data: dict) -> str:
    song_data["created_at"] = datetime.now()
    song_data["modified_at"] = datetime.now()
    return await insert("song", song_data)
    
# 노래 검색 (페이징)
async def search_songs(query: str, skip: int, limit: int) -> List[dict]:
    return await get_many("song", {"title": {"$regex": query, "$options": "i"}}, skip, limit)
'''