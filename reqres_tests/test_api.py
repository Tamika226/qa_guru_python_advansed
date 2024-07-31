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


@pytest.mark.parametrize("size", [1, 5, 10])
@pytest.mark.parametrize("page", [1, 2, 5])
def test_users_pagination(app_url, users, size, page):
    response = requests.get(f"{app_url}/api/users/?page={page}&size={size}")
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    for user in response_json["items"]:
        User.model_validate(user)
    assert response_json["total"] == len(users)
    assert len(response_json["items"]) == max(0,len(users)-(page-1)*size) if len(users)-(page-1)*size < size else size
    assert response_json["items"][0]["id"] == 1 if page == 1 else size*(page-1)


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
