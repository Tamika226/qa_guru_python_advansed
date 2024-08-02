import datetime

from pydantic import BaseModel


class NewUser(BaseModel):
    name: str
    job: str


class CreatedUser(NewUser):
    id: int
    createdAt: datetime.datetime


class UpdatedUser(NewUser):
    updatedAt: datetime.datetime
