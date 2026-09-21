def test_auth_register_returns_token(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "username": "newuser01",
            "password": "secret123",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_auth_login_returns_token(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "user01",
            "password": "secret123",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
