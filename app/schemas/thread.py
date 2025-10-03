from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.user import UserResponse
from app.schemas.message import MessageResponse


class ThreadBase(BaseModel):
    thread_type: str = "direct"
    title: Optional[str] = None


class ThreadCreate(ThreadBase):
    participant_ids: List[int]


class ThreadParticipantResponse(BaseModel):
    user: UserResponse
    joined_at: datetime
    is_admin: bool

    class Config:
        from_attributes = True


class ThreadResponse(ThreadBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime]
    last_message_at: Optional[datetime]
    is_active: bool
    participants: List[ThreadParticipantResponse]
    last_message: Optional[MessageResponse] = None
    unread_count: int = 0

    class Config:
        from_attributes = True


class ThreadListResponse(BaseModel):
    threads: List[ThreadResponse]
    total: int