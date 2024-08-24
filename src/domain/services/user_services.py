from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import select

from config import Settings
from repositories.models import User
from domain.services.auth_services import validate_unique


def get_user(user_id, db: Session):
    stmt = select(User).filter(User.id == user_id)

    try:
        user = db.execute(stmt).scalar_one()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}"
        )

    return user


def update_user(user_id, request, db: Session):
    user = get_user(user_id, db)

    try:
        if validate_unique("email", request.email, db):
            user.email = request.email
        if validate_unique("user_name", request.user_name, db):
            user.user_name = request.user_name
        is_valid = Settings.PWD_CONTEXT.verify(user.password, request.password)
        if is_valid:
            user.password = Settings.PWD_CONTEXT.hash(request.password)

        user.updated_at = datetime.now(datetime.UTC)

        db.flush()

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Integrity Error occurred during update the new Loan item.: {str(e)}")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during update: {str(e)}")
    else:
        db.commit()
        db.refresh(user)
        return user
