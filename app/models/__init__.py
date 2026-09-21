from sqlmodel import SQLModel

from .agent import Agent
from .delivery import Delivery
from .delivery_status_history import DeliveryStatusHistory
from .dispute import Dispute
from .notification import Notification
from .payment import Payment
from .rating import Rating
from .tracking import Tracking
from .user import User
from . import agent as agent_module
from . import delivery as delivery_module
from . import delivery_status_history as history_module
from . import dispute as dispute_module
from . import notification as notification_module
from . import payment as payment_module
from . import rating as rating_module
from . import tracking as tracking_module
from . import user as user_module

agent_module.User = User
agent_module.Delivery = Delivery
user_module.Agent = Agent
user_module.Delivery = Delivery
user_module.Dispute = Dispute
user_module.Notification = Notification
user_module.Payment = Payment
user_module.Rating = Rating
delivery_module.User = User
delivery_module.Agent = Agent
delivery_module.DeliveryStatusHistory = DeliveryStatusHistory
delivery_module.Dispute = Dispute
delivery_module.Payment = Payment
delivery_module.Rating = Rating
delivery_module.Tracking = Tracking
history_module.Delivery = Delivery
dispute_module.Delivery = Delivery
dispute_module.User = User
notification_module.User = User
payment_module.Delivery = Delivery
payment_module.User = User
rating_module.Delivery = Delivery
rating_module.User = User
tracking_module.Delivery = Delivery

__all__ = [
    "Agent",
    "Delivery",
    "DeliveryStatusHistory",
    "Dispute",
    "Notification",
    "Payment",
    "Rating",
    "SQLModel",
    "Tracking",
    "User",
]
