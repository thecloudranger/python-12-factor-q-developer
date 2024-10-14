import pytest
from app import app, db, Task


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()


def test_hello(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the Task Management App!" in response.data


def test_add_task(client):
    response = client.post("/tasks", json={"task": "Test task"})
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["task"] == "Test task"
    assert response.json["completed"] == False


def test_get_tasks(client):
    client.post("/tasks", json={"task": "Test task 1"})
    client.post("/tasks", json={"task": "Test task 2"})

    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["task"] == "Test task 1"
    assert response.json[1]["task"] == "Test task 2"


def test_update_task(client):
    response = client.post("/tasks", json={"task": "Test task"})
    task_id = response.json["id"]

    response = client.put(f"/tasks/{task_id}", json={"completed": True})
    assert response.status_code == 200
    assert response.json["completed"] == True


def test_delete_task(client):
    response = client.post("/tasks", json={"task": "Test task"})
    task_id = response.json["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    response = client.get("/tasks")
    assert len(response.json) == 0
