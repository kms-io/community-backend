from datetime import date

from fastapi import Depends, Header, HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session

from database import get_db_session
from repositories.models import User
from config import Settings


def get_db():
    try:
        session = get_db_session()
        yield session
    finally:
        session.close()


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
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise credentials_exception
    if not user.is_valid:
        raise credentials_exception
    return user


def get_current_active_user(user: User = Depends(get_current_user)):
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return user
