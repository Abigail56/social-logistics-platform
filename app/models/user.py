from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .agent import Agent
    from .delivery import Delivery
    from .dispute import Dispute
    from .notification import Notification
    from .payment import Payment
    from .rating import Rating


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    username: str = Field(index=True, unique=True, nullable=False)
    password_hash: str = Field(nullable=False)
    role: str = Field(default="customer", nullable=False)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
    )

    agent: Optional["Agent"] = Relationship(back_populates="user")
    deliveries: list["Delivery"] = Relationship(back_populates="customer")
    disputes: list["Dispute"] = Relationship(back_populates="opened_by")
    notifications: list["Notification"] = Relationship(back_populates="user")
    payments: list["Payment"] = Relationship(back_populates="user")
    ratings: list["Rating"] = Relationship(back_populates="user")
