import requests
from http import HTTPStatus
from reqres_fast_api.models.AppStatus import AppStatus


def test_status(app_url):
    response = requests.get(f"{app_url}/api/status")
    AppStatus.model_validate(response.json())
    assert response.status_code == HTTPStatus.OK
    assert response.json()["database"]
