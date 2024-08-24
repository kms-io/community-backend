from datetime import datetime as _datetime

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str = Field(..., title="email", description="이메일", example="John@example.com")
    user_name: str = Field(..., title="user_name", description="사용자 이름", example="John")
    is_active: bool = Field(False, title="is_active", description="활성 상태", example=True)


class User(UserBase):
    id: int = Field(..., title="user_id", description="사용자 ID", example=1, ge=0)
    created_at: _datetime = Field(..., title="create_at", description="생성일시", example=_datetime.now())
    updated_at: _datetime = Field(..., title="create_at", description="생성일시", example=_datetime.now())


class UserCreate(BaseModel):
    email: str = Field(..., title="email", description="이메일", example="John@example.com")
    user_name: str = Field(..., title="user_name", description="사용자 이름", example="John")
    password: str = Field(..., title="password", description="비밀번호", example="qwerty123")


class UserUpdate(BaseModel):
    email: str | None = Field(..., title="email", description="이메일", example="John@example.com")
    user_name: str | None = Field(..., title="user_name", description="사용자 이름", example="John")
    password: str | None = Field(..., title="password", description="비밀번호", example="qwerty123")
