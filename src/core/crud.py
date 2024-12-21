from src.core.database import db
from bson import ObjectId
from typing import List, Optional, Any

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

# UPDATE: 특정 ID의 데이터 수정
async def update_by_id(collection: str, obj_id: str, update_data: dict) -> bool:
    result = await db[collection].update_one({"_id": ObjectId(obj_id)}, {"$set": update_data})
    return result.modified_count > 0

# DELETE: 특정 ID의 데이터 삭제
async def delete_by_id(collection: str, obj_id: str) -> bool:
    result = await db[collection].delete_one({"_id": ObjectId(obj_id)})
    return result.deleted_count > 0

# COUNT
async def count_by_column(collection_name: str, column_name: str, value: Any) -> int:
    collection = db[collection_name]
    count = await collection.count_documents({column_name: value})
    return count