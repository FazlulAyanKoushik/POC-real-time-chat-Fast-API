from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class MessageBase(BaseModel):
    content: str
    message_type: str = "text"
    media_url: Optional[str] = None


class MessageCreate(MessageBase):
    thread_id: int


class MessageUpdate(BaseModel):
    is_read: Optional[bool] = None


class MessageResponse(MessageBase):
    id: int
    thread_id: int
    sender_id: int
    is_read: bool
    read_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class MessageListResponse(BaseModel):
    messages: List[MessageResponse]
    total: int
    has_more: bool