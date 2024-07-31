from fastapi import APIRouter, HTTPException
from fastapi_pagination import paginate, Page
from reqres_fast_api.models.User import User, UserCreate, UserUpdate
from reqres_fast_api.database import users

from http import HTTPStatus

router = APIRouter(prefix="/api/users")


@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    user = users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/",  status_code=HTTPStatus.OK)
def get_users() -> Page[User]:
    return paginate(users.get_users())


@router.post("/", status_code=HTTPStatus.CREATED)
def create_user(user: User) -> User:
    UserCreate.model_validate(user.model_dump())
    return users.create_user(user)


@router.patch("/{user_id}", status_code=HTTPStatus.OK)
def update_user(user_id: int, user: User) -> User:
    if not users.get_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    UserUpdate.model_validate(user.model_dump())
    return users.update_user(user_id, user)


@router.delete("/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int):
    if not users.get_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    users.delete_user(user_id)
    return {"User deleted"}
