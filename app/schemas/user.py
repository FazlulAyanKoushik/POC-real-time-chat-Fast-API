from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    profile_picture: Optional[str] = None

class UserLogin(UserBase):
    username: str
    password: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    profile_picture: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_online: bool
    last_seen: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class UserProfile(UserResponse):
    friends_count: int = 0