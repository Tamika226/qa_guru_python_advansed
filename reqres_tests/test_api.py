import requests
import pytest
import random
from http import HTTPStatus
from reqres_fast_api.models.User import User, UserCreate, UserUpdate
import json
from pydantic import EmailStr, HttpUrl
from faker import Faker

fake = Faker("ru_RU")


@pytest.fixture
def create_user_model():
    def make(
        first_name: str = fake.first_name(),
        last_name: str = fake.last_name(),
        email: EmailStr = fake.email(),
        avatar: HttpUrl = fake.url(),
        **rest
    ):
        created_user = UserUpdate(
            first_name=first_name, last_name=last_name, email=email, avatar=avatar, **rest
        )
        return created_user
    return make


@pytest.fixture
def new_user(app_url, create_user_model):
    user = create_user_model()
    response = requests.post(f"{app_url}/api/users/", data=user.json())
    assert response.status_code == HTTPStatus.CREATED
    return User(**response.json())


@pytest.fixture(scope="module")
def fill_test_data(app_url):
    with open("users.json") as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = requests.post(f'{app_url}/api/users', json=user)
        api_users.append(response.json())
    user_ids = [user["id"] for user in api_users]
    yield user_ids
    for user_id in user_ids:
        requests.delete(f'{app_url}/api/users/{user_id}')


@pytest.fixture
def get_random_id_from_db(fill_test_data):
    return random.choice(fill_test_data)


@pytest.mark.parametrize("size", [1, 5, 10])
@pytest.mark.parametrize("page", [1, 2, 5])
def test_users_pagination(app_url, fill_test_data, size, page):
    response = requests.get(f"{app_url}/api/users/?page={page}&size={size}")
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    for user in response_json["items"]:
        User.model_validate(user)
    assert response_json["total"] == len(fill_test_data)
    assert len(response_json["items"]) == max(0, len(fill_test_data)-(page-1)*size) if len(fill_test_data)-(page-1)*size < size else size
    if response_json["items"] is None:
        assert response_json["items"][0]["id"] == fill_test_data[0] if page == 1 else fill_test_data[size*(page-1)]


def test_users(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK
    users_in_request = response.json()["items"]
    for user in users_in_request:
        User.model_validate(user)


def test_users_no_duplicates(fill_test_data):
    assert len(fill_test_data) == len(set(fill_test_data))


def test_user(app_url, get_random_id_from_db):
    response = requests.get(f"{app_url}/api/users/{get_random_id_from_db}")
    assert response.status_code == HTTPStatus.OK
    User.model_validate(response.json())


@pytest.mark.parametrize("user_id", [0, 13])
def test_user_nonexisting_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_user_invalid_values(app_url):
    response = requests.get(f"{app_url}/api/users/test")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_user(app_url, create_user_model):
    user = create_user_model()
    response = requests.post(f"{app_url}/api/users/", data=user.json())
    assert response.status_code == HTTPStatus.CREATED
    response_get = requests.get(f'{app_url}/api/users/{response.json()["id"]}')
    assert response_get.json() == response.json()


def test_update_user(app_url, new_user, create_user_model):
    updated_user = create_user_model(first_name="Chizhik")
    response = requests.patch(f'{app_url}/api/users/{new_user.id}', data=updated_user.json())
    assert response.status_code == HTTPStatus.OK
    response_get = requests.get(f'{app_url}/api/users/{response.json()["id"]}')
    assert response_get.json() == response.json()


def test_delete_user(app_url, new_user):
    response = requests.delete(f'{app_url}/api/users/{new_user.id}')
    assert response.status_code == HTTPStatus.OK
    response_get = requests.get(f'{app_url}/api/users/{new_user.id}')
    assert response_get.status_code == HTTPStatus.NOT_FOUND
