from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas import UserCreate
from app.security import hash_password


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    statement = select(User).where(
        User.email == email
    )

    return db.scalar(statement)


def create_user(
    db: Session,
    data: UserCreate,
) -> User:
    user = User(
        email=data.email,
        hashed_password=hash_password(
            data.password
        ),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user