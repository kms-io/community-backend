import os
from typing import ClassVar

import sshtunnel
from dotenv import load_dotenv
from passlib.context import CryptContext
from pydantic_settings import BaseSettings

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

    DB_HOST: str = os.getenv("EXP_DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("EXP_DB_PORT", 3306))
    DB_NAME: str = os.getenv("EXP_DB_NAME", "prod_db")
    DB_USER: str = os.getenv("EXP_DB_USER", "root")
    DB_PASSWORD: str = os.getenv("EXP_DB_PASSWORD", "1235")

    @property
    def DATABASE_URL(self):
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()

def create_ssh_tunnel():
    try:
        tunnel = sshtunnel.SSHTunnelForwarder(
            ('52.79.###.###', 22),  # EC2 endpoint
            ssh_username='ubuntu',
            ssh_pkey='kms-io.pem',  # SSH private key path
            remote_bind_address=('kms-io-db.####.ap-northeast-2.rds.amazonaws.com', 3306),  # RDS endpoint
            local_bind_address=('localhost', 13306)
        )
        tunnel.start()
        # Update DB port to use tunnel
        settings.DB_PORT = 13306
        settings.DB_HOST = 'localhost'
        return tunnel
    except Exception as e:
        print(f"Failed to create SSH tunnel: {e}")
        return None

ssh_tunnel = create_ssh_tunnel()
