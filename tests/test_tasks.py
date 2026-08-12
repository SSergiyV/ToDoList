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

def test_get_tasks_sort_by_title_asc(client):
    client.post("/tasks", json={"title": "Charlie"})
    client.post("/tasks", json={"title": "Alpha"})
    client.post("/tasks", json={"title": "Bravo"})

    response = client.get("/tasks?sort_by=title&order=asc")

    assert response.status_code == 200

    data = response.json()

    titles = [task["title"] for task in data]

    assert titles == ["Alpha", "Bravo", "Charlie"]

def test_get_tasks_sort_by_title_desc(client):
    client.post("/tasks", json={"title": "Charlie"})
    client.post("/tasks", json={"title": "Alpha"})
    client.post("/tasks", json={"title": "Bravo"})

    response = client.get("/tasks?sort_by=title&order=desc")

    assert response.status_code == 200

    data = response.json()

    titles = [task["title"] for task in data]

    assert titles == ["Charlie", "Bravo", "Alpha"]

def test_get_tasks_sort_by_created_at_desc(client):
    first = client.post(
        "/tasks",
        json={"title": "First task"}
    ).json()

    second = client.post(
        "/tasks",
        json={"title": "Second task"}
    ).json()

    response = client.get(
        "/tasks?sort_by=created_at&order=desc"
    )

    assert response.status_code == 200

    data = response.json()

    assert data[0]["id"] == second["id"]
    assert data[1]["id"] == first["id"]

def test_get_tasks_pagination_with_sorting(client):
    client.post("/tasks", json={"title": "Charlie"})
    client.post("/tasks", json={"title": "Alpha"})
    client.post("/tasks", json={"title": "Echo"})
    client.post("/tasks", json={"title": "Bravo"})

    response = client.get(
        "/tasks?skip=1&limit=2&sort_by=title&order=asc"
    )

    assert response.status_code == 200

    data = response.json()

    titles = [task["title"] for task in data]

    assert titles == ["Bravo", "Charlie"]

def test_get_tasks_filter_done_true(client):
    first = client.post(
        "/tasks",
        json={"title": "Done task"}
    ).json()

    client.post(
        "/tasks",
        json={"title": "Another task"}
    )

    update_response = client.patch(
        f"/tasks/{first['id']}",
        json={"done": True}
    )

    assert update_response.status_code == 200

    response = client.get("/tasks?done=true")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Done task"
    assert data[0]["done"] is True

def test_get_tasks_filter_done_false(client):
    first = client.post(
        "/tasks",
        json={"title": "Done task"}
    ).json()

    client.post(
        "/tasks",
        json={"title": "Pending task"}
    )

    update_response = client.patch(
        f"/tasks/{first['id']}",
        json={"done": True}
    )

    assert update_response.status_code == 200

    response = client.get("/tasks?done=false")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Pending task"
    assert data[0]["done"] is False

def test_get_tasks_filter_sort_and_paginate(client):
    tasks = [
        ("Charlie", True),
        ("Alpha", False),
        ("Echo", True),
        ("Bravo", True),
    ]

    for title, done in tasks:
        task = client.post(
            "/tasks",
            json={"title": title}
        ).json()

        if done:
            response = client.patch(
                f"/tasks/{task['id']}",
                json={"done": True}
            )
            assert response.status_code == 200

    response = client.get(
        "/tasks?done=true&sort_by=title&order=asc&skip=1&limit=2"
    )

    assert response.status_code == 200

    data = response.json()

    titles = [task["title"] for task in data]

    assert titles == ["Charlie", "Echo"]

def test_get_tasks_search(client):
    client.post("/tasks", json={"title": "Learn Python"})
    client.post("/tasks", json={"title": "Learn FastAPI"})
    client.post("/tasks", json={"title": "Learn SQLAlchemy"})

    response = client.get("/tasks?search=Python")

    assert response.status_code == 200

    data = response.json()

    titles = [task["title"] for task in data]

    assert titles == ["Learn Python"]

def test_get_tasks_search_case_insensitive(client):
    client.post("/tasks", json={"title": "Learn Python"})
    client.post("/tasks", json={"title": "Python FastAPI"})
    client.post("/tasks", json={"title": "Learn SQLAlchemy"})

    response = client.get("/tasks?search=python")

    assert response.status_code == 200

    data = response.json()

    titles = [task["title"] for task in data]

    assert titles == [
        "Learn Python",
        "Python FastAPI"
    ]

def test_get_tasks_search_and_done_filter(client):
    first = client.post(
        "/tasks",
        json={"title": "Learn Python"}
    ).json()

    client.post(
        "/tasks",
        json={"title": "Learn FastAPI"}
    )

    response = client.patch(
        f"/tasks/{first['id']}",
        json={"done": True}
    )

    assert response.status_code == 200

    response = client.get(
        "/tasks?search=Python&done=true"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Learn Python"
    assert data[0]["done"] is True

def test_get_tasks_search_sort_and_paginate(client):
    tasks = [
        "Python Basics",
        "Python FastAPI",
        "Python Advanced",
        "JavaScript Basics",
    ]

    for title in tasks:
        client.post("/tasks", json={"title": title})

    response = client.get(
        "/tasks?search=python&sort_by=title&order=asc&skip=1&limit=1"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Python Basics"