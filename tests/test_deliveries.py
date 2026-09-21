def test_create_delivery_returns_requested_status(client):
    response = client.post(
        "/deliveries/",
        json={
            "customer_id": 1,
            "pickup_location": "Lagos",
            "destination": "Ibadan",
            "package_details": "Books",
            "total_amount": 2500,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "REQUESTED"
    assert body["pickup_location"] == "Lagos"


def test_update_delivery_valid_transition(client):
    response = client.patch(
        "/deliveries/1",
        json={"status": "ACCEPTED"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ACCEPTED"


def test_update_delivery_invalid_transition(client):
    response = client.patch(
        "/deliveries/1",
        json={"status": "DELIVERED"},
    )
    assert response.status_code == 400
