import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User


def register_user(
    db: Session,
    organization_id: uuid.UUID,
    role_id: uuid.UUID,
    name: str,
    email: str,
    password: str,
) -> User:

    existing_user = db.scalar(
        select(User).where(
            User.email == email
        )
    )

    if existing_user:
        raise ValueError("Email already registered")

    user = User(
        organization_id=organization_id,
        role_id=role_id,
        name=name,
        email=email,
        password_hash=hash_password(password),
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:

    user = db.scalar(
        select(User).where(
            User.email == email
        )
    )

    if not user:
        return None

    if not user.is_active:
        return None

    if not verify_password(
        password,
        user.password_hash,
    ):
        return None

    return user


def create_user_token(user: User) -> str:
    return create_access_token(
        str(user.id)
    )