from pydantic import BaseModel, EmailStr
from typing import List, Optional


class User(BaseModel):
    id: int | None = None
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    avatar: str | None = None


class UserList(BaseModel):
    items: List[User]
    total: int
