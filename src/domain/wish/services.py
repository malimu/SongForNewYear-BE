from src.core.database import db
from src.core.crud import insert, get_by_id, get_many
from datetime import datetime
from typing import List
from src.exceptions.custom_exceptions import CustomException
from src.exceptions.error_codes import ErrorCode

from src.domain.wish.gpt_categorize import categorize_wish
from src.domain.song.services import get_song_by_song_index

# 소원의 카테고리 분류 및 노래 추천
async def process_wish(wish):
    if not wish.content:
        raise CustomException(ErrorCode.MISSING_PARAMETER)
    
    # 양옆 공백 제거
    wish.content = wish.content.strip()
    wish.nickname = wish.nickname.strip()
    
    # 이미 동일한 내용의 소원이 존재하는지 확인
    existing_wish = await db["wish"].find_one({
        "nickname": wish.nickname,
        "content": wish.content
    })
    
    if existing_wish:
        existing_wish_song = await db["song"].find_one({
            "_id": existing_wish["song_id"]
        })
        song_id = str(existing_wish["_id"])
        return {
            "wish_id": song_id,
            "nickname": existing_wish["nickname"],
            "wish": existing_wish["content"],
            "category": existing_wish_song["category"],  # category는 기존 소원에서 가져와야 할 수도 있음
            "recommended_song": {
                "title": existing_wish_song["title"],
                "artist": existing_wish_song["artist"],
                "lyrics": existing_wish_song["lyrics"],
                "cover_path": existing_wish_song["cover_path"],
                "recommend_time": existing_wish_song["start_time"],
                "youtube_path": existing_wish_song["youtube_path"],
            },
            "wishes_count": await count_wishes_by_song_id(song_id)
        }


    # 카테고리 분류 및 추천 노래 가져오기
    category_data = await categorize_wish(wish.content)  # {"category": "...", "song_index": ...}
    recommended_song = await get_song_by_song_index(category_data["song_index"])
    
    # 노래 추천 시점 계산
    start_time = datetime.strptime(recommended_song["start_time"], "%H:%M:%S")
    midnight = datetime.strptime("00:00:00", "%H:%M:%S")
    recommend_time = midnight - start_time

    # 소원 데이터 생성 및 반환
    created_wish = await create_wish(
        nickname=wish.nickname,
        content=wish.content,
        song_id=recommended_song["_id"],
        is_displayed=wish.is_displayed,
    )
    song_id = str(created_wish["_id"])

    return {
        "wish_id": song_id,
        "nickname": created_wish["nickname"],
        "wish": created_wish["content"],
        "category": recommended_song["category"],
        "recommended_song": {
            "title": recommended_song["title"],
            "artist": recommended_song["artist"],
            "lyrics": recommended_song["lyrics"],
            "cover_path": recommended_song["cover_path"],
            "recommend_time": str(recommend_time),
            "youtube_path": recommended_song["youtube_path"],
        },
        "wishes_count": count_wishes_by_song_id(song_id)
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
    created_wish = await db["wish"].find_one({"_id": result.inserted_id})
    return created_wish

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
