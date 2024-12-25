from src.core.database import db
from src.core.crud import insert, get_by_id
from datetime import datetime
from typing import List
from src.exceptions.custom_exceptions import CustomException
from src.exceptions.error_codes import ErrorCode

from src.domain.wish.gpt_categorize import categorize_wish
from src.domain.song.services import get_song_by_song_index, get_random_song_by_tag

from src.domain.wish.keywords_mapping import keyword_to_tag

# 소원 처리 메인 함수
async def process_wish(wish):
    validate_wish(wish)

    existing_wish = await find_existing_wish(wish)
    if existing_wish:
        return await handle_existing_wish(existing_wish)

    # 키워드 기반 태그 검색 및 추천
    keyword_recommendation = await recommend_by_keyword(wish.content)
    if keyword_recommendation:
        return keyword_recommendation

    # AI로 태그+제목 기반 추천
    return await categorize_and_recommend(wish)

## 유효성 검사 함수
def validate_wish(wish):
    if not wish.content:
        raise CustomException(ErrorCode.MISSING_PARAMETER)
    wish.content = wish.content.strip()
    wish.nickname = wish.nickname.strip()

## 기존 소원 찾기
async def find_existing_wish(wish):
    return await db["wish"].find_one({
        "nickname": wish.nickname,
        "content": wish.content
    })

## 기존 소원 처리
async def handle_existing_wish(existing_wish):
    existing_wish_song = await db["song"].find_one({
        "_id": existing_wish["song_id"]
    })
    song_id = str(existing_wish["_id"])
    return {
        "wish_id": song_id,
        "nickname": existing_wish["nickname"],
        "wish": existing_wish["content"],
        "category": existing_wish_song["category"],
        "recommended_song": format_song_data(existing_wish_song),
        "wishes_count": await count_wishes_by_song_id(song_id)
    }

## 키워드 기반 추천
async def recommend_by_keyword(content):
    for keyword, tag in keyword_to_tag.items():
        if keyword in content:
            recommended_song = await get_random_song_by_tag(tag)
            if recommended_song:
                return {
                    "wish_id": None,
                    "nickname": None,
                    "wish": content,
                    "category": recommended_song["category"],
                    "recommended_song": format_song_data(recommended_song),
                    "wishes_count": await count_wishes_by_song_id(recommended_song["_id"])
                }
    return None

## 태그 분류 및 추천
async def categorize_and_recommend(wish):
    category_data = await categorize_wish(wish.content)
    
    recommended_song = await get_song_by_song_index(category_data["song_index"])

    # 노래 추천 시점 계산
    recommend_time = calculate_recommend_time(recommended_song["start_time"])

    # 소원 데이터 생성
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
            **format_song_data(recommended_song),
            "recommend_time": str(recommend_time),
        },
        "wishes_count": await count_wishes_by_song_id(song_id)
    }

## 노래 데이터 포맷팅
def format_song_data(song):
    if "lyrics" in song and isinstance(song["lyrics"], str):
            song["lyrics"] = song["lyrics"].replace("\\n", "\n")
    return {
        "title": song["title"],
        "artist": song["artist"],
        "lyrics": song["lyrics"],
        "cover_path": song["cover_path"],
        "recommend_time": song["start_time"],
        "youtube_path": song["youtube_path"]
    }


## 추천 시간 계산
def calculate_recommend_time(start_time):
    start_time_dt = datetime.strptime(start_time, "%H:%M:%S")
    midnight = datetime.strptime("00:00:00", "%H:%M:%S")
    return midnight - start_time_dt


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


# 랜덤 소원 가져오기
async def get_random_wishes(limit: int = 4) -> List[dict]:
    wishes = await db["wish"].aggregate([{"$sample": {"size": limit}}]).to_list(length=limit)
    for wish in wishes:
        song = await get_by_id("song", wish["song_id"])
        if song:
            category = song.get("category")
            if category is None:
                wish["category"] = "WEALTH" # 에러를 발생시키는 대신 임의의 카테고리 값을 삽입
            wish["category"] = category
        else:
            wish["category"] = "HAPPINESS" # 에러를 발생시키는 대신 임의의 카테고리 값을 삽입
    return wishes


# 특정 소원 가져오기
async def get_wish_by_id(_id: str) -> dict:
    return await get_by_id("wish", _id)


# 특정 노래의 wish 갯수 세기
async def count_wishes_by_song_id(_id: str) -> int:
    count = await db.wish.count_documents({"song_id": _id})
    return count
