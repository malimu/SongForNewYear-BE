from src.core.database import db
from bson import ObjectId
from typing import List, Optional

# CREATE: 데이터 삽입
async def insert(collection: str, data: dict) -> str:
    result = await db[collection].insert_one(data)
    return str(result.inserted_id)

# READ: 특정 ID로 데이터 가져오기
async def get_by_id(collection: str, obj_id: str) -> Optional[dict]:
    result = await db[collection].find_one({"_id": ObjectId(obj_id)})
    return result

# READ: 조건으로 데이터 가져오기 (페이징 지원)
async def get_many(collection: str, filter: dict, skip: int = 0, limit: int = 10) -> List[dict]:
    results = await db[collection].find(filter).skip(skip).limit(limit).to_list(length=limit)
    return results