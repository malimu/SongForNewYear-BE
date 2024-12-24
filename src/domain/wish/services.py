from src.core.database import db
from src.core.crud import insert, get_by_id, get_many
from datetime import datetime
from typing import List
from src.exceptions.custom_exceptions import CustomException
from src.exceptions.error_codes import ErrorCode

from src.domain.wish.categorize import categorize_wish
from src.domain.song.services import get_random_song_by_category

# 소원의 카테고리 분류 및 노래 추천
async def process_wish(wish):
    if not wish.content:
        raise CustomException(
            error_code=ErrorCode.MISSING_PARAMETER,
            status_code=400,
        )
    # 챗지피티로 카테고리 분류
    category = await categorize_wish(wish.content)
    # 곡 추천 
    recommended_song = await get_random_song_by_category(category)
    if not recommended_song:
        raise CustomException(
            error_code=ErrorCode.SONG_NOT_FOUND,
            status_code=404,
        )
    # 노래 들어야할 시점 계산
    start_time = datetime.strptime(recommended_song["startTime"], "%H:%M:%S")
    midnight = datetime.strptime("00:00:00", "%H:%M:%S")
    recommend_time = midnight - start_time
    # 소원 생성 
    _id = await create_wish(
        nickname=wish.nickname,
        content=wish.content,
        song_id=recommended_song["song_id"],
        is_displayed=wish.is_displayed,
    )
    return {
        "_id": _id,
        "nickname": wish.nickname,
        "wish": wish.content,
        "recommended_song": {
            "title": recommended_song["title"],
            "artist": recommended_song["artist"],
            "lyrics": recommended_song["lyrics"],
            "cover_path": recommended_song["cover_path"],
            "recommend_time": str(recommend_time),
            "youtube_path": recommended_song["youtube_path"],
        }
    }

# 소원 생성
async def create_wish(nickname: str, content: str, song_id: str, is_displayed: bool) -> str:
    wish_data = {
        "nickname": nickname,
        "content": content,
        "is_displayed": is_displayed,
        "created_at": datetime.now(),
        "song_id": song_id,
    }
    result = await db["wish"].insert_one(wish_data)
    return str(result.inserted_id)

# 특정 소원 가져오기
async def get_wish_by_id(_id: str) -> dict:
    return await get_by_id("wish", _id)

# 랜덤 소원 가져오기
async def get_random_wishes(limit: int = 4) -> List[dict]:
    # MongoDB의 $sample 사용 (별도 crud 함수 필요할 수도 있음)
    wishes = await db["wish"].aggregate([{"$sample": {"size": limit}}]).to_list(length=limit)
    return wishes

# 특정 노래의 wish 갯수 세기
async def count_wishes_by_song_id(_id: str) -> int:
    wishes = await get_many("wish", {"song_id": _id}, 0, 0)  # 모든 wish를 가져옴
    return len(wishes)
