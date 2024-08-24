from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get(
    "/{user_id}",
    summary="사용자 정보 조회",
)
async def get_user(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pass


@router.put(
    "/{user_id}",
    summary="사용자 정보 수정",
)
async def update_user(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pass


@router.delete(
    "/{user_id}",
    summary="사용자 정보 삭제",
)
async def delete_user(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pass
