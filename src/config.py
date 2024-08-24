import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from passlib.context import CryptContext
from typing import ClassVar


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Settings(BaseSettings):
    # 환경 설정
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_EXPIRATION_TIME_MINUTES: int = int(os.getenv("JWT_ACCESS_EXPIRATION_TIME_MINUTES", 30))
    JWT_REFRESH_EXPIRATION_TIME_DAYS: int = int(os.getenv("JWT_REFRESH_EXPIRATION_TIME_DAYS", 30))

    PWD_CONTEXT: ClassVar[CryptContext] = CryptContext(schemes=["bcrypt"], deprecated="auto")

    DB_HOST: str = os.getenv("EXP_DB_HOST")
    DB_PORT: int = int(os.getenv("EXP_DB_PORT"))
    DB_NAME: str = os.getenv("EXP_DB_NAME")
    DB_USER: str = os.getenv("EXP_DB_USER")
    DB_PASSWORD: str = os.getenv("EXP_DB_PASSWORD")

    @property
    def DATABASE_URL(self):
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()