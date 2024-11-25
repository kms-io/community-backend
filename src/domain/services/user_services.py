from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from config import Settings
from domain.services.auth_services import validate_unique
from repositories.models import User


def get_user(user_id, db: Session):
    stmt = select(User).where(User.id == user_id)

    try:
        user = db.execute(stmt).scalar_one()

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        ) from None

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}"
        ) from e

    return user


def update_user(user_id, request, db: Session):
    user = get_user(user_id, db)

    try:
        if validate_unique("email", request.email, db) and request.email is not None:  # request.email이 존재하고
            user.email = request.email
        if validate_unique("user_name", request.user_name, db) and request.user_name is not None:  # request.user_name이 존재하고
            user.user_name = request.user_name

        user.updated_at = datetime.now(timezone.utc) + timedelta(hours=9)

        db.flush()

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Integrity Error occurred during update the item.: {str(e)}")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during update: {str(e)}")
    else:
        db.commit()
        db.refresh(user)
        return user
