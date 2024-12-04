from typing import AsyncGenerator

from fastapi import Depends, Header, HTTPException, status
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from config import Settings
from database import get_db_session
from exceptions import InactiveUserException
from repositories.models import User


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db_session():
        try:
            yield session
        finally:
            await session.close()


async def get_current_user(token=Header(None), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WW-Authenticate": "Bearer"},
    )
    payload = jwt.decode(token, key=Settings().JWT_SECRET_KEY, algorithms=Settings().JWT_ALGORITHM)
    user_id: int = int(payload.get("sub"))
    if user_id is None:
        raise credentials_exception
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()

    if user is None:
        raise credentials_exception
    if not user.is_valid:
        raise credentials_exception
    return user


def get_current_active_user(user: User = Depends(get_current_user)):
    if not user.is_active:
        raise InactiveUserException()
    return user
