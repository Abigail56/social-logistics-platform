from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


class Notification(SQLModel, table=True):
    __tablename__ = "notifications"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    title: str = Field(nullable=False)
    message: str = Field(nullable=False)
    is_read: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user: Optional["User"] = Relationship(back_populates="notifications")
