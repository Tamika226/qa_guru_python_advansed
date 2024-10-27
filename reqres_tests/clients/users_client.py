from httpx import Client, HTTPStatusError
from pydantic import ValidationError

from reqres_tests.clients.settings import Settings
from reqres_tests.helpers.session import BaseSession
from reqres_tests.models.users import User, UserList


class UserApiClient(BaseSession):

    def __init__(self, settings: Settings):
        super().__init__(base_url=settings.base_url)

    def get_user(self, user_id: int) -> User:
        try:
            response = self.request('get',f"/api/users/{user_id}")
            response.raise_for_status()
            return User(**response.json())
        except HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError("User not found")
            raise e

    def get_users(self) -> UserList:
        try:
            response = self.request('get',"/api/users/")
            response.raise_for_status()
            return UserList(**response.json())
        except HTTPStatusError as e:
            raise e

    def create_user(self, user: User) -> User:
        try:
            response = self.request('post',"/api/users/", json=user.model_dump())
            response.raise_for_status()
            return User(**response.json())
        except ValidationError as e:
            raise ValueError("Invalid user data")
        except HTTPStatusError as e:
            raise e

    def update_user(self, user_id: int, user: User) -> User:
        try:
            response = self.request('patch',f"/api/{user_id}", json=user.model_dump(exclude_unset=True))
            response.raise_for_status()
            return User(**response.json())
        except HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError("User not found")
            raise e

    def delete_user(self, user_id: int):
        try:
            response = self.request('delete',f"/{user_id}")
            response.raise_for_status()
            return {"message": "User deleted"}
        except HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError("User not found")
            raise e
