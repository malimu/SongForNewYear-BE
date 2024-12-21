from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI: str = "mongodb://localhost:27017"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()