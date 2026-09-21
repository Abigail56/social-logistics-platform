from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .delivery import Delivery
    from .user import User


class Rating(SQLModel, table=True):
    __tablename__ = "ratings"

    id: int | None = Field(default=None, primary_key=True)
    delivery_id: int = Field(foreign_key="deliveries.id", nullable=False, index=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    score: int = Field(default=5, nullable=False)
    comment: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    delivery: Optional["Delivery"] = Relationship(back_populates="ratings")
    user: Optional["User"] = Relationship(back_populates="ratings")
