from datetime import datetime, timedelta, timezone

from domain.services.token_services import create_user_tokens
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import select

from config import Settings
from repositories.models import User


def validate_unique(type: str, value: str, db: Session):
    # type은 email 혹은 user_name. 즉 검증하고 싶은 타입이 들어옴
    # value는 요청하고자 하는 데이터 값
    user_attr = getattr(User, type)

    stmt = select(User).filter(user_attr == value)
    try:
        v = db.execute(stmt).scalar_one_or_none()
        if v is not None:
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


def register(request, db: Session):

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


def login(request, db: Session):
    stmt = select(User).filter(User.email == request.email)
    try:
        user = db.execute(stmt).scalar_one()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not exists"
        )

    is_valid = Settings.PWD_CONTEXT.verify(request.password, user.password)

    user_info_required = False
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not exists"
        )
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is invalid"
        )

    token_response = create_user_tokens(user.id)

    if user_info_required:
        return {
            "token": token_response,
            "user_info_required": True
        }
    else:
        return {
            "token": token_response,
            "user": {
                "id": user.id,
                "user_name": user.user_name,
                "is_active": user.is_active,
                "email": user.email
            }
        }
