from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    profile_picture = Column(Text)
    is_active = Column(Boolean, default=True)
    is_online = Column(Boolean, default=False)
    last_seen = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships - using string references to avoid circular imports
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    thread_participants = relationship("ThreadParticipant", back_populates="user")

    # Friendship relationships
    initiated_friendships = relationship(
        "Friendship",
        foreign_keys="Friendship.user_id",
        back_populates="user"
    )
    received_friendships = relationship(
        "Friendship",
        foreign_keys="Friendship.friend_id",
        back_populates="friend"
    )


class Friendship(Base):
    __tablename__ = "friendships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    friend_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="initiated_friendships")
    friend = relationship("User", foreign_keys=[friend_id], back_populates="received_friendships")