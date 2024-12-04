from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import domain.schemas.auth_schemas as auth_schemas
import domain.services.auth_services as auth_service
from config import Settings
from dependencies import get_current_user, get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

settings = Settings()


@router.post(
    "/register",
    response_model=auth_schemas.RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="신규 사용자 등록",
    description="""신규 사용자 등록""",
    response_description={
        status.HTTP_201_CREATED: {"description": "User created"}
    }
)
async def register(
    request: auth_schemas.RegisterRequest,
    db: Session = Depends(get_db)
):
    result = auth_service.register(request, db)
    return result


@router.post(
    "/login",
    response_model=auth_schemas.LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="사용자 로그인",
    description="""사용자 로그인""",
    response_description={
        status.HTTP_200_OK: {"description": "User logined"}
    }
)
async def login(
    request: auth_schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    result = auth_service.login(request, db)
    return result


@router.put(
    "/set-password",
    response_model=auth_schemas.UserInfo,
    status_code=status.HTTP_200_OK,
    summary="사용자 비밀번호 재설정",
    description="""사용자 비밀번호 재설정""",
    response_description={
        status.HTTP_200_OK: {"description": "Password successfully changed"}
    }
)
async def set_password(
    request: auth_schemas.SetPasswordRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = auth_service.set_password(current_user.id, request, db)
    return result


@router.put(
    "/reset-password",
    response_model=auth_schemas.UserInfo,
    status_code=status.HTTP_200_OK,
    summary="사용자 비밀번호 초기화",
    description="""사용자 비밀번호 초기화""",
    response_description={
        status.HTTP_200_OK: {"description": "Password successfully changed"}
    }
)
async def reset_password(
    request: auth_schemas.ResetPasswordRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = auth_service.reset_password(current_user.id, request, db)
    return result
