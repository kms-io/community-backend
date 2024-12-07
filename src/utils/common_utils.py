from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import InternalServerErrorException
from repositories.models import User


def validate_unique(type: str, value: str, db: AsyncSession):
    # type은 email 혹은 user_name. 즉 검증하고 싶은 타입이 들어옴
    # value는 요청하고자 하는 데이터 값
    user_attr = getattr(User, type)

    stmt = select(User).where(user_attr == value)
    try:
        v = db.execute(stmt).scalar_one_or_none()
        if v is not None:  # 새로 추가할 데이터이기에 db에 존재한다면
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{type} already exists"
            )
    except Exception as e:
        InternalServerErrorException(e)
    return True
