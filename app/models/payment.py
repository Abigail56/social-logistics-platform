from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .delivery import Delivery
    from .user import User


class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    id: int | None = Field(default=None, primary_key=True)
    delivery_id: int = Field(foreign_key="deliveries.id", nullable=False, index=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    amount: float = Field(default=0.0, nullable=False)
    currency: str = Field(default="USD", nullable=False)
    status: str = Field(default="PENDING", nullable=False)
    provider: str = Field(default="local", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    paid_at: datetime | None = Field(default=None)

    delivery: Optional["Delivery"] = Relationship(back_populates="payments")
    user: Optional["User"] = Relationship(back_populates="payments")
