from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "song_for_new_year"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# 인덱스 설정
async def init_db():
    await db["wishes"].create_index([("createdAt", ASCENDING)])