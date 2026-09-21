from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .delivery import Delivery


class DeliveryStatusHistory(SQLModel, table=True):
    __tablename__ = "delivery_status_history"

    id: int | None = Field(default=None, primary_key=True)
    delivery_id: int = Field(foreign_key="deliveries.id", nullable=False, index=True)
    previous_status: str | None = Field(default=None)
    new_status: str = Field(nullable=False)
    changed_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    delivery: Optional["Delivery"] = Relationship(back_populates="status_history")
