from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config import Settings
from dependencies import get_current_user, get_db
from domain.schemas.auth_schemas import (
    RequestPostUserLogin,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    ResetPasswordRequest,
    SetPasswordRequest,
    UserInfo,
)
from domain.services.auth_services import (
    service_login_with_firebase,
    service_login_with_username,
    service_register,
    service_reset_password,
    service_set_password,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

settings = Settings()


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="신규 사용자 등록",
    description="""신규 사용자 등록""",
    response_description={
        status.HTTP_201_CREATED: {"description": "User created"},
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    result = service_register(request, db)
    return result


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="사용자 로그인",
    description="""사용자 로그인""",
    response_description={
        status.HTTP_200_OK: {"description": "User logined"},
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)
async def login(
    request: RequestPostUserLogin,
    db: Session = Depends(get_db)
):
    if settings.ENVIRONMENT == "development":
        result = await service_login_with_username(request, db)
    elif settings.ENVIRONMENT == "production":
        result = await service_login_with_firebase(request, db)
    return result


@router.put(
    "/set-password",
    response_model=UserInfo,
    status_code=status.HTTP_200_OK,
    summary="사용자 비밀번호 재설정",
    description="""사용자 비밀번호 재설정""",
    response_description={
        status.HTTP_200_OK: {"description": "Password successfully changed"}
    }
)
async def set_password(
    request: SetPasswordRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = service_set_password(current_user.id, request, db)
    return result


@router.put(
    "/reset-password",
    response_model=UserInfo,
    status_code=status.HTTP_200_OK,
    summary="사용자 비밀번호 초기화",
    description="""사용자 비밀번호 초기화""",
    response_description={
        status.HTTP_200_OK: {"description": "Password successfully changed"}
    }
)
async def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = service_reset_password(current_user.id, request, db)
    return result
