from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Test task"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Test task"
    assert data["done"] is False
    assert "id" in data

def test_get_tasks(client):
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})

    response = client.get("/tasks")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"

def test_get_task(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Task for GET"
        }
    )

    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Task for GET"
    assert data["done"] is False

def test_get_task_not_found(client):
    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_create_duplicate_task(client):
    client.post(
        "/tasks",
        json={
            "title": "Duplicate task"
        }
    )

    response = client.post(
        "/tasks",
        json={
            "title": "Duplicate task"
        }
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Task with this title already exists"

def test_update_task(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Old title"
        }
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "title": "New title",
            "done": True
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "New title"
    assert data["done"] is True

def test_update_task_not_found(client):
    response = client.patch(
        "/tasks/999999",
        json={
            "title": "New title"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_delete_task(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Task to delete"
        }
    )

    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted"

    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 404

def test_delete_task_not_found(client):
    response = client.delete("/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_get_tasks_pagination(client):
    for i in range(5):
        client.post(
            "/tasks",
            json={"title": f"Pagination task {i}"}
        )

    response = client.get("/tasks?skip=1&limit=2")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "Pagination task 1"
    assert data[1]["title"] == "Pagination task 2"

def test_get_tasks_limit_validation(client):
    response = client.get("/tasks?limit=101")

    assert response.status_code == 422

def test_get_tasks_skip_validation(client):
    response = client.get("/tasks?skip=-1")

    assert response.status_code == 422

