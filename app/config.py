import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Chat"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database
    DB_TYPE: str = os.getenv("DB_TYPE", "sqlite")

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Message Limits
    NON_FRIEND_MESSAGE_LIMIT: int = 20

    @property
    def DATABASE_URL(self) -> str | None:
        if self.DB_TYPE == "sqlite":
            return "sqlite+aiosqlite:///./chat.db"
        else:
            return os.getenv("DATABASE_URL")

    class Config:
        case_sensitive = True


settings = Settings()