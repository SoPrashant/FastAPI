from ..routers.users import get_db
from fastapi import status
from .utils import app, override_get_db, client, TestingSessionLocal, Users


app.dependency_overrides[get_db] = override_get_db


def test_read_all_authenticated(test_user):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "name": "exampleUser",
            "email": "exampleUser123@gmail.com",
            "phone": "9462733220",
            "id": 1,
        }
    ]


def test_read_one_authenticated(test_user):
    response = client.get("/user/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "name": "exampleUser",
        "email": "exampleUser123@gmail.com",
        "phone": "9462733220",
        "id": 1,
    }


def test_read_one_authenticated_not_found():
    response = client.get("/user/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}


def test_create_user(test_user):
    request_data = {
        "name": "New User!",
        "email": "newuser@email.com",
        "phone": "6745231098",
    }

    response = client.post("/user/", json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 2).first()
    assert model.name == request_data.get("name")
    assert model.email == request_data.get("email")
    assert model.phone == request_data.get("phone")


def test_partial_update_user(test_user):
    request_data = {"email": "updateduser@hotmail.com"}

    response = client.patch("/user/1/", json=request_data)
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 1).first()
    assert model.email == request_data.get("email")


def test_partial_update_user_not_found(test_user):
    request_data = {
        "email": "updateduser@hotmail.com",
    }

    response = client.patch("/user/999/", json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}


def test_update_user(test_user):
    request_data = {
        "name": "updated User!",
        "email": "updateduser@hotmail.com",
        "phone": "9078564312",
    }

    response = client.put("/user/1/", json=request_data)
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 1).first()
    assert model.name == request_data.get("name")
    assert model.email == request_data.get("email")
    assert model.phone == request_data.get("phone")


def test_update_user_not_found(test_user):
    request_data = {
        "name": "updated User!",
        "email": "updateduser@hotmail.com",
        "phone": "9078564312",
    }

    response = client.put("/user/999/", json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}


def test_delete_user(test_user):
    response = client.delete("/user/1")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 1).first()
    assert model is None


def test_delete_user_not_found():
    response = client.delete("/user/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}
