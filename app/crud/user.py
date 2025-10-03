from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.auth.jwt import get_password_hash
from app.models.user import User, Friendship
from app.schemas.user import UserCreate, UserUpdate


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    # return db.query(User).filter(User.username == username).first()
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=str(user.email),
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate) -> User:
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def add_friend(db: AsyncSession, user_id: int, friend_id: int) -> Friendship:
    friendship = Friendship(user_id=user_id, friend_id=friend_id)
    db.add(friendship)
    db.commit()
    db.refresh(friendship)
    return friendship


def remove_friend(db: AsyncSession, user_id: int, friend_id: int) -> bool:
    friendship = db.query(Friendship).filter(
        ((Friendship.user_id == user_id) & (Friendship.friend_id == friend_id)) |
        ((Friendship.user_id == friend_id) & (Friendship.friend_id == user_id))
    ).first()

    if friendship:
        db.delete(friendship)
        db.commit()
        return True
    return False


def are_friends(db: AsyncSession, user_id: int, other_user_id: int) -> bool:
    friendship = db.query(Friendship).filter(
        ((Friendship.user_id == user_id) & (Friendship.friend_id == other_user_id)) |
        ((Friendship.user_id == other_user_id) & (Friendship.friend_id == user_id))
    ).first()
    return friendship is not None


def get_friends(db: AsyncSession, user_id: int) -> List[User]:
    friends1 = db.query(User).join(Friendship, Friendship.friend_id == User.id).filter(
        Friendship.user_id == user_id).all()
    friends2 = db.query(User).join(Friendship, Friendship.user_id == User.id).filter(
        Friendship.friend_id == user_id).all()
    return list(set(friends1 + friends2))