from fastapi import status
from .utils import *
from ..routers.users import get_current_user, get_db

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get('/users')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'adminuser'
    assert response.json()['email'] == 'adminuser@email.com'
    assert response.json()['first_name'] == 'admin'
    assert response.json()['last_name'] == 'user'
    assert response.json()['role'] == 'admin'


def test_change_password_success(test_user):
    response = client.put('/users/password', json={"password": "adminpassword",
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put('/users/password', json={"password": "wrong_password",
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change'}