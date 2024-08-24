from datetime import datetime, timedelta, timezone

from jose import jwt

from config import Settings


def create_jwt(
    data: dict,
    secret_key: str,
    algorithm: str,
    expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encode_jwt


def create_user_tokens(user_id: int) -> dict:
    access_token_expires = timedelta(minutes=Settings().JWT_ACCESS_EXPIRATION_TIME_MINUTES)
    access_token = create_jwt(
        data={"sub": str(user_id)},
        secret_key=Settings().JWT_SECRET_KEY,
        algorithm=Settings().JWT_ALGORITHM,
        expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=Settings().JWT_REFRESH_EXPIRATION_TIME_DAYS)
    refresh_token = create_jwt(
        data={"sub": str(user_id)},
        secret_key=Settings().JWT_SECRET_KEY,
        algorithm=Settings().JWT_ALGORITHM,
        expires_delta=refresh_token_expires
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
