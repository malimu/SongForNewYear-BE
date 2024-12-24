from src.core.database import db
from src.core.crud import get_many, get_by_id, get_by_column_value, count_by_column
from src.exceptions.custom_exceptions import CustomException
from src.exceptions.error_codes import ErrorCode
from typing import Optional, List

# 전체 노래 목록 가져오기
async def get_all_songs(skip: int, limit: int) -> List[dict]:
    filter_query = {}
    songs = await get_many("song", filter_query, skip, limit)
    return normalize_lyrics(songs)

# 카테고리별 노래 목록 가져오기
async def get_songs_by_category(category: Optional[str], skip: int, limit: int) -> List[dict]:
    filter_query = {"category": category} if category else {}
    songs = await get_many("song", filter_query, skip, limit)
    return normalize_lyrics(songs)

# 카테고리에 맞는 총 노래 수를 반환
async def get_total_songs_count(category: Optional[str]) -> int:
    filter_query = {"category": category} if category else {}
    return await count_by_column("song", filter_query)

# _id로 노래 가져오기
async def get_song_by_obj_id(_id: object):
    song = await get_by_id("song", _id)
    return normalize_lyrics([song])[0] if song else None

# song_index로 노래 가져오기
async def get_song_by_song_index(song_index: int):
    song = await get_by_column_value("song", "song_index", song_index)
    return normalize_lyrics([song])[0] if song else None

# 특정 카테고리에서 랜덤으로 한 곡을 선택
async def get_random_song_by_category(category: str) -> dict:
    result = await db["song"].aggregate([
        {"$match": {"category": category}},
        {"$sample": {"size": 1}}
    ]).to_list(length=1)

    # 결과가 비어 있는 경우
    if not result:
        raise CustomException(ErrorCode.SONG_NOT_FOUND)
    return normalize_lyrics(result)[0]

# 공통 메서드: normalize_lyrics (역슬래시 이스케이프 방지)
def normalize_lyrics(songs: List[dict]) -> List[dict]:
    for song in songs:
        if "lyrics" in song and isinstance(song["lyrics"], str):
            song["lyrics"] = song["lyrics"].replace("\\n", "\n")
    return songs

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