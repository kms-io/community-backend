from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from config import Settings
from domain.schemas.auth_schemas import (
    RequestPostUserLogin_dev,
    RequestPostUserRegister,
    ResponsePostUserLogin,
    ResponsePostUserRegister,
)
from domain.services.exceptions import UserNotFoundException
from domain.services.token_services import create_user_tokens
from repositories.models import User
from utils.common_utils import validate_unique


async def service_register(
    request: RequestPostUserRegister,
    db: AsyncSession
) -> ResponsePostUserRegister:

    # 이메일 중복 체크
    validate_unique("email", request.email, db)

    # 사용자 이름 중복 체크
    validate_unique("user_name", request.user_name, db)

    current_time = datetime.now(ZoneInfo("Asia/Seoul"))

    user = User(
        email=request.email,
        user_name=request.user_name,
        created_at=current_time,
        updated_at=current_time,
        is_active=False
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    response = ResponsePostUserRegister(
        user_id=user.id,
        user_name=user.user_name,
        email=user.email,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

    return response


async def service_login_with_username(
    request: RequestPostUserLogin_dev,
    db: AsyncSession
) -> ResponsePostUserLogin:
    stmt = select(User).where(User.user_name == request.user_name)
    try:
        result = await db.execute(stmt)
        user = result.scalar_one()

    except NoResultFound as e:
        raise UserNotFoundException() from e

    token_response = create_user_tokens(user.id)

    return {
        "token": token_response,
        "user": {
            "id": user.id,
            "user_name": user.user_name,
            "is_active": user.is_active,
            "email": user.email
        }
    }

async def service_login_with_firebase(request, db: Session):
    pass


async def service_set_password(user_id, request, db: Session):
    stmt = select(User).where(User.id == user_id)
    try:
        user = db.execute(stmt).scalar_one
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not exists"
        ) from None

    if request.old_password != request.confirm_old_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The entered passwords do not match"
        )
    try:
        is_valid = Settings.PWD_CONTEXT.verify(request.old_password, user.password)

        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is invalid"
            )
        else:
            user.password = Settings.PWD_CONTEXT.hash(request.new_password)

        user.updated_at = datetime.now(timezone.utc) + timedelta(hours=9)

        db.flush()

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Integrity Error occurred during update the item.: {str(e)}")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during update: {str(e)}")
    else:
        db.commit()
        db.refresh(user)
        return user


async def service_reset_password(user_id, request, db: Session):
    stmt = select(User).where(User.id == user_id)

    try:
        user = db.execute(stmt).scalar_one
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not exists"
        )

    try:
        user.password = Settings.PWD_CONTEXT.hash(request.new_password)
        user.updated_at = datetime.now(timezone.utc) + timedelta(hours=9)

        db.flush()

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Integrity Error occurred during update the item.: {str(e)}")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during update: {str(e)}")
    else:
        db.commit()
        db.refresh(user)
        return user
