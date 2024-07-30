import requests
import pytest
from http import HTTPStatus
from reqres_fast_api.models.User import User, UserCreate, UserUpdate
import json


@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK
    return response.json()["items"]

@pytest.fixture
def fill_test_data(app_url):
    with open("users.json") as f:
        test_data_users = json.load(f)
    for user in test_data_users:
        requests.post(f'{app_url}/api/user', json = user)

def test_users(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK
    users_in_request = response.json()["items"]
    for user in users_in_request:
        User.model_validate(user)


@pytest.mark.parametrize("limit", [1, 5, 10])
@pytest.mark.parametrize("offset", [0, 2, 5, 10])
def test_users_pagination(app_url, users, limit, offset):
    response = requests.get(f"{app_url}/api/users/?limit={limit}&offset={offset}")
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    for user in response_json["items"]:
        User.model_validate(user)
    assert response_json["total"] == len(users)
    assert len(response_json["items"]) == len(users)-offset < limit if len(users)-offset < limit else limit
    assert response_json["items"][0]["id"] == offset+1


def test_users_no_duplicates(users):
    users_ids = [user["id"] for user in users]
    assert len(users_ids) == len(set(users_ids))


@pytest.mark.parametrize("user_id", [1, 2, 11])
def test_user(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
    User.model_validate(response.json())


@pytest.mark.parametrize("user_id", [0, 13])
def test_user_nonexisting_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_user_invalid_values(app_url):
    response = requests.get(f"{app_url}/api/users/test")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
