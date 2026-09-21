from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .delivery import Delivery
    from .user import User


class Agent(SQLModel, table=True):
    __tablename__ = "agents"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True, nullable=False)
    is_available: bool = Field(default=True)
    rating: float = Field(default=0.0)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
    )

    user: Optional["User"] = Relationship(back_populates="agent")
    deliveries: list["Delivery"] = Relationship(back_populates="agent")
