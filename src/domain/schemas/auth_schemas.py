from pydantic import BaseModel, EmailStr, Field


class UserInfo(BaseModel):
    id: int
    user_name: str
    is_active: bool
    email: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RequestPostUserLogin(BaseModel):
    email: str = Field(example="test@test.com")
    password: str = Field(example="qwerty123")

class RequestPostUserLogin_Dev(BaseModel):
    user_name: str = Field(example="테스트", min_length=2, max_length=30)


class LoginResponse(BaseModel):
    token: TokenResponse = None
    user: UserInfo = None


class RegisterRequest(BaseModel):
    user_name: str = Field(example="테스트")
    email: EmailStr = Field(example="test@test.com")
    password: str = Field(example="qwerty123")


class RegisterResponse(BaseModel):
    token: TokenResponse = None
    user: UserInfo = None


class SetPasswordRequest(BaseModel):
    old_password: str = Field(example="qwerty123")
    confirm_old_password: str = Field(example="qwerty123")
    new_password: str = Field(example="qwerty12345")


class ResetPasswordRequest(BaseModel):
    new_password: str = Field(example="qwerty")
