import requests
import random
import pytest
from reqres_tests import utils
from pytest_schema import schema
from reqres_tests import schemas
from mimesis import Person
from mimesis.locales import Locale


class TestApi:
    def test_get_users(self):
        response = requests.get(utils.URL+"/api/users")
        assert response.status_code == 200
        data = response.json()
        assert schema(schemas.all_users_get) == data
        assert len(data["data"]) == 5
        assert data["data"][0]["id"] == 1

    @pytest.mark.parametrize("page, expected_first_element", [(1, 1), (2, 6)])
    def test_get_users_with_paging(self, page, expected_first_element):
        response = requests.get(utils.URL+"/api/users", params={"page": page})
        data = response.json()
        assert response.status_code == 200
        assert schema(schemas.all_users_get) == data
        assert len(data["data"]) == 5
        assert data["data"][0]["id"] == expected_first_element

    def test_get_user(self):
        response = requests.get(utils.URL+"/api/users/"+str(random.randint(1, 10)))
        assert response.status_code == 200
        assert schema(schemas.user_get) == response.json()

    def test_create_user(self):
        new_user = {"name": Person(Locale.RU).first_name(), "job": Person(Locale.RU).occupation()}
        response = requests.post(utils.URL+"/api/users/", json=new_user)
        data = response.json()
        assert response.status_code == 201
        assert schema(schemas.created_user) == data
        assert data["name"] == new_user["name"]
        assert data["job"] == new_user["job"]

    def test_update_user_put(self):
        updated_user = {"name": Person(Locale.RU).first_name(), "job": Person(Locale.RU).occupation()}
        response = requests.put(utils.URL+"/api/users/"+str(random.randint(1, 100)), json=updated_user)
        data = response.json()
        assert response.status_code == 200
        assert schema(schemas.update_user) == data
        assert data["name"] == updated_user["name"]
        assert data["job"] == updated_user["job"]

    def test_update_user_patch(self):
        updated_user = {"name": Person(Locale.RU).first_name(), "job": Person(Locale.RU).occupation()}
        response = requests.patch(utils.URL+"/api/users/"+str(random.randint(1, 100)), json=updated_user)
        data = response.json()
        assert response.status_code == 200
        assert schema(schemas.update_user) == data
        assert data["name"] == updated_user["name"]
        assert data["job"] == updated_user["job"]

    def test_delete_user(self):
        response = requests.delete(utils.URL+"/api/users/"+str(random.randint(1, 100)))
        assert response.status_code == 204
