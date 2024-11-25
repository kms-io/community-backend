from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings


class EngineConnection:
    def __init__(self):
        SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
        self.engine = create_async_engine(
            SQLALCHEMY_DATABASE_URL,
            pool_recycle=500,
            connect_args={"connect_timeout": 100}
        )
        self.session_local = sessionmaker(
            autoflush=False,
            autocommit=False,
            bind=self.engine,
            class_=AsyncSession
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_local() as session:
            yield session

    async def get_connection(self):
        async with self.engine.connect() as connection:
            yield connection


engine_conn = EngineConnection()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in engine_conn.get_session():
        yield session
