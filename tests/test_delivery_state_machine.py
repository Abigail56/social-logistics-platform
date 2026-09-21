import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.delivery_state_machine import (
    DeliveryStateMachine,
    DeliveryStatus,
)


@pytest.mark.parametrize(
    ("start", "next_status"),
    [
        (DeliveryStatus.REQUESTED, DeliveryStatus.ACCEPTED),
        (DeliveryStatus.ACCEPTED, DeliveryStatus.PICKED_UP),
        (DeliveryStatus.PICKED_UP, DeliveryStatus.IN_TRANSIT),
        (DeliveryStatus.IN_TRANSIT, DeliveryStatus.DELIVERED),
        (DeliveryStatus.REQUESTED, DeliveryStatus.CANCELLED),
        (DeliveryStatus.ACCEPTED, DeliveryStatus.CANCELLED),
    ],
)
def test_valid_delivery_transitions(start, next_status):
    state_machine = DeliveryStateMachine(start)
    assert state_machine.can_transition(next_status)
    assert state_machine.transition_to(next_status) == next_status


def test_invalid_transition_is_rejected():
    state_machine = DeliveryStateMachine(DeliveryStatus.REQUESTED)
    assert not state_machine.can_transition(DeliveryStatus.DELIVERED)
    with pytest.raises(ValueError):
        state_machine.transition_to(DeliveryStatus.DELIVERED)


def test_terminal_state_cannot_progress():
    state_machine = DeliveryStateMachine(DeliveryStatus.DELIVERED)
    assert state_machine.is_terminal()
    assert not state_machine.can_transition(DeliveryStatus.CANCELLED)


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
