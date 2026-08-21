def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "user@example.com"
    assert "id" in data
    assert "password" not in data
    assert "password_hash" not in data

def test_register_duplicate_email_returns_409(client):
    payload = {
        "email": "user@example.com",
        "password": "password123",
    }

    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == "User with this email already exists"