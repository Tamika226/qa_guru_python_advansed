from fastapi import APIRouter, HTTPException
from fastapi_pagination import paginate, Page
from reqres_fast_api.models.User import User
from reqres_fast_api.users_load import users

from http import HTTPStatus

router = APIRouter(prefix="/api/users")


@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if any(filter(lambda user: user['id'] == user_id, users)):
        return next((user for user in users if user["id"] == user_id), False)
    raise HTTPException(status_code=404, detail="User not found")


@router.get("/",  status_code=HTTPStatus.OK)
def get_users() -> Page[User]:
    return paginate(users)
