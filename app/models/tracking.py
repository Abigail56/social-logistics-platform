from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .delivery import Delivery


class Tracking(SQLModel, table=True):
    __tablename__ = "tracking"

    id: int | None = Field(default=None, primary_key=True)
    delivery_id: int = Field(foreign_key="deliveries.id", nullable=False, index=True)
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)
    location_name: str | None = Field(default=None)
    status: str = Field(default="ACTIVE", nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    delivery: Optional["Delivery"] = Relationship(back_populates="tracking")
