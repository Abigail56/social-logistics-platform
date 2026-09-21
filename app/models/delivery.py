from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .agent import Agent
    from .delivery_status_history import DeliveryStatusHistory
    from .dispute import Dispute
    from .payment import Payment
    from .rating import Rating
    from .tracking import Tracking
    from .user import User


class Delivery(SQLModel, table=True):
    __tablename__ = "deliveries"

    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="users.id", nullable=False)
    agent_id: int | None = Field(default=None, foreign_key="agents.id")
    pickup_location: str = Field(nullable=False)
    destination: str = Field(nullable=False)
    package_details: str = Field(nullable=False)
    status: str = Field(default="REQUESTED", nullable=False, index=True)
    total_amount: float = Field(default=0.0, nullable=False)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
    )
    accepted_at: datetime | None = Field(default=None)
    picked_up_at: datetime | None = Field(default=None)
    delivered_at: datetime | None = Field(default=None)
    cancelled_at: datetime | None = Field(default=None)

    customer: Optional["User"] = Relationship(back_populates="deliveries")
    agent: Optional["Agent"] = Relationship(back_populates="deliveries")
    status_history: list["DeliveryStatusHistory"] = Relationship(
        back_populates="delivery"
    )
    disputes: list["Dispute"] = Relationship(back_populates="delivery")
    payments: list["Payment"] = Relationship(back_populates="delivery")
    ratings: list["Rating"] = Relationship(back_populates="delivery")
    tracking: list["Tracking"] = Relationship(back_populates="delivery")
