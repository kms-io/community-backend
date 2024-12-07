# ruff: noqa: E501

from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from sqlalchemy.sql import func

from repositories.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    user_name = Column(String(30), unique=True, nullable=False, index=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_deleted = Column(Boolean, nullable=False, default=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    verification_code = Column(String(10), nullable=True)
