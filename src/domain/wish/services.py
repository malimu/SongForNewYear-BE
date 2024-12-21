from src.core.crud import insert, get_by_id, get_many
from datetime import datetime
from typing import List

# 소원 생성
async def create_wish(nickname: str, content: str, song_id: str) -> str:
    wish_data = {
        "nickname": nickname,
        "content": content,
        "is_displayed": True,
        "created_at": datetime.now(),
        "song_id": song_id,
    }
    return await insert("wishes", wish_data)

# 특정 소원 가져오기
async def get_wish_by_id(wish_id: str) -> dict:
    return await get_by_id("wishes", wish_id)

# 랜덤 소원 가져오기
async def get_random_wishes(limit: int = 4) -> List[dict]:
    # MongoDB의 $sample 사용 (별도 crud 함수 필요할 수도 있음)
    wishes = await db["wishes"].aggregate([{"$sample": {"size": limit}}]).to_list(length=limit)
    return wishes


# 특정 노래의 wish 갯수 세기
async def count_wishes_by_song_id(song_id: str) -> int:
    wishes = await get_many("wishes", {"song_id": song_id}, 0, 0)  # 모든 wish를 가져옴
    return len(wishes)
