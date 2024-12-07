from datetime import date, timedelta
from datetime import datetime as _datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Unpack


class ItemBase(BaseModel):
    created_at: _datetime = Field(title="created_at", description="생성일시", example=_datetime.now())
    updated_at: _datetime = Field(title="updated_at", description="수정일시", example=_datetime.now())
    is_valid: bool = Field(title="is_valid", description="유효 여부", example=True)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__annotations__['id'] = int
        cls.id = Field(..., title="id", description=f'{cls.__name__.lower()} id', example=1, ge=0)
