from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .delivery import Delivery
    from .user import User


class Dispute(SQLModel, table=True):
    __tablename__ = "disputes"

    id: int | None = Field(default=None, primary_key=True)
    delivery_id: int = Field(foreign_key="deliveries.id", nullable=False, index=True)
    opened_by_user_id: int = Field(foreign_key="users.id", nullable=False)
    reason: str = Field(nullable=False)
    status: str = Field(default="OPEN", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    resolved_at: datetime | None = Field(default=None)

    delivery: Optional["Delivery"] = Relationship(back_populates="disputes")
    opened_by: Optional["User"] = Relationship(back_populates="disputes")
