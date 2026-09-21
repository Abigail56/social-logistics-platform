from __future__ import annotations

from enum import Enum
from typing import ClassVar


class DeliveryStatus(str, Enum):
    REQUESTED = "REQUESTED"
    ACCEPTED = "ACCEPTED"
    PICKED_UP = "PICKED_UP"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class DeliveryStateMachine:
    transitions: ClassVar[dict[DeliveryStatus, set[DeliveryStatus]]] = {
        DeliveryStatus.REQUESTED: {
            DeliveryStatus.ACCEPTED,
            DeliveryStatus.CANCELLED,
        },
        DeliveryStatus.ACCEPTED: {
            DeliveryStatus.PICKED_UP,
            DeliveryStatus.CANCELLED,
        },
        DeliveryStatus.PICKED_UP: {
            DeliveryStatus.IN_TRANSIT,
            DeliveryStatus.CANCELLED,
        },
        DeliveryStatus.IN_TRANSIT: {DeliveryStatus.DELIVERED},
        DeliveryStatus.DELIVERED: set(),
        DeliveryStatus.CANCELLED: set(),
    }

    def __init__(self, current_status: DeliveryStatus):
        self.current_status = current_status

    def can_transition(self, next_status: DeliveryStatus) -> bool:
        allowed = self.transitions.get(self.current_status, set())
        return next_status in allowed

    def transition_to(self, next_status: DeliveryStatus) -> DeliveryStatus:
        if not self.can_transition(next_status):
            raise ValueError(
                f"Invalid transition from {self.current_status.value} "
                f"to {next_status.value}"
            )
        self.current_status = next_status
        return self.current_status

    def is_terminal(self) -> bool:
        return self.current_status in {
            DeliveryStatus.DELIVERED,
            DeliveryStatus.CANCELLED,
        }
