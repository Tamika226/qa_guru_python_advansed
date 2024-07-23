import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str


class Support(BaseModel):
    url: str
    text: str


class UserGetResponse(BaseModel):
    data: User
    support: Support


class UsersGetResponse(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[User]
    support: Support


class NewUser(BaseModel):
    name: str
    job: str


class CreatedUser(NewUser):
    id: int
    createdAt: datetime.datetime


class UpdatedUser(NewUser):
    updatedAt: datetime.datetime


class Login(BaseModel):
    email: str
    password: str | None = None


class LoginSuccess(BaseModel):
    token: str

