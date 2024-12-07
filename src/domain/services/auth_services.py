from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, MultipleResultsFound, NoResultFound
from sqlalchemy.orm import Session

from config import Settings
from domain.schemas.auth_schemas import RequestPostUserLogin_Dev
from domain.services.exceptions import UserNotFoundException
from domain.services.token_services import create_user_tokens
from repositories.models import User


def validate_unique(type: str, value: str, db: Session):
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during service: {str(e)}"
        )
    return True


async def service_register(request, db: Session):

    # 이메일 중복 체크
    validate_unique("email", request.email, db)

    # 사용자 이름 중복 체크
    validate_unique("user_name", request.user_name, db)

    hashed_password = Settings.PWD_CONTEXT.hash(request.password)

    current_time = datetime.now(timezone.utc) + timedelta(hours=9)

    user = User(
        email=request.email,
        user_name=request.user_name,
        password=hashed_password,
        created_at=current_time,
        updated_at=current_time,
        is_active=False
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "user": {
            "id": user.id,
            "user_name": user.user_name,
            "is_active": user.is_active,
            "email": user.email,
            "created_at": current_time,
            "updated_at": current_time,
        }
    }


async def service_login_with_username(
    request: RequestPostUserLogin_Dev,
    db: Session
):
    stmt = select(User).where(User.user_name == request.user_name)
    try:
        user = db.execute(stmt).scalar_one()

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
