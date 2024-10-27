import json

import pytest

from reqres_tests.clients.settings import Settings
from reqres_tests.clients.users_client import UserApiClient
from reqres_tests.models.users import User


def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="dev", help="Укажите окружение: dev, prod, staging."
    )


@pytest.fixture(scope="session")
def config(request):
    env = request.config.getoption("--env")

    if env == "dev":
        return Settings(base_url="http://127.0.0.1:8002")
    elif env == "staging":
        return Settings(base_url="http://127.0.0.1:8002")
    elif env == "prod":
        return Settings(base_url="http://127.0.0.1:8002")
    else:
        raise ValueError(f"Неизвестное окружение: {env}")


@pytest.fixture(scope="session")
def user_client(config):
    return UserApiClient(settings=config)


@pytest.fixture(scope="session", autouse=True)
def create_users_for_test(user_client):
    with open('../user.json', 'r', encoding='utf-8') as file:
        users_data = json.load(file)

    for user_data in users_data:
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            avatar=user_data['avatar']
        )
        user_client.create_user(user)
