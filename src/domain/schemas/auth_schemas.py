from pydantic import BaseModel, Field, EmailStr


class UserInfo(BaseModel):
    id: int
    user_name: str
    is_active: bool
    email: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class LoginRequest(BaseModel):
    email: str = Field(example="test@test.com")
    password: str = Field(example="qwerty123")


class LoginResponse(BaseModel):
    token: TokenResponse = None
    user: UserInfo = None
    user_info_required: bool = False


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
