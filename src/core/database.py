from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from pydantic_settings import BaseSettings

# Config - Settings 클래스 정의
class Settings(BaseSettings):
    DB_URI: str
    DB_NAME: str
    openai_api_key: str
    
    class Config:
        env_file = ".env"

# 환경 변수 값 가져오기
settings = Settings()

# DB 클라이언트 초기화
client = AsyncIOMotorClient(settings.DB_URI)
db = client[settings.DB_NAME]

# 인덱스 설정
async def init_db():
    await db["wishes"].create_index([("created_at", ASCENDING)])