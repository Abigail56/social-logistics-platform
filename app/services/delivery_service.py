from app.services.delivery_state_machine import (
    DeliveryStateMachine,
    DeliveryStatus,
)


class DeliveryService:
    @staticmethod
    def can_update_status(current_status: str, next_status: str) -> bool:
        current = DeliveryStatus(current_status)
        target = DeliveryStatus(next_status)
        return DeliveryStateMachine(current).can_transition(target)

    @staticmethod
    def transition_status(current_status: str, next_status: str) -> str:
        current = DeliveryStatus(current_status)
        target = DeliveryStatus(next_status)
        return DeliveryStateMachine(current).transition_to(target).value
