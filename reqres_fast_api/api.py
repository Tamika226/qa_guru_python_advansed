import datetime
import math
import random
import secrets

from fastapi import FastAPI, HTTPException, Response
from reqres_fast_api import models
from reqres_fast_api import db_sample

app = FastAPI()


@app.get("/")
async def home():
    return {"data": "Hello! This is reqres.io copy written by FastPai"}


@app.get("/api/users/{user_id}", response_model=models.UserGetResponse)
def get_single_user(user_id: int):
    if any(filter(lambda user: user['id'] == user_id, db_sample.users)):
        user = next((user for user in db_sample.users if user["id"] == user_id), False)
        return models.UserGetResponse(data=user, support=db_sample.support_data)
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/api/users", response_model=models.UsersGetResponse)
def get_list_users(page: int = 1, per_page: int = 5):
    get_response = models.UsersGetResponse(
        page=page,
        per_page=per_page,
        total=len(db_sample.users),
        total_pages=math.ceil(len(db_sample.users)/per_page),
        data=db_sample.users[(page-1)*per_page:page*per_page if len(db_sample.users) >= page*per_page-1 else len(db_sample.users)],
        support=db_sample.support_data)
    return get_response


@app.post("/api/users", response_model=models.CreatedUser, status_code=201)
def create_user(user: models.NewUser):
    new_user = models.CreatedUser(
        name=user.name,
        job=user.job,
        id=random.randint(1, 100),
        createdAt=datetime.datetime.now())
    return new_user


@app.put("/api/users/{user_id}", response_model=models.UpdatedUser)
@app.patch("/api/users/{user_id}", response_model=models.UpdatedUser)
def update_user(user: models.NewUser):
    updated_user = models.UpdatedUser(
        name=user.name,
        job=user.job,
        updatedAt=datetime.datetime.now())
    return updated_user


@app.delete("/api/users/{user_id}")
def delete_user():
    return Response(status_code=204)


@app.post("/api/register", response_model=models.LoginSuccess)
@app.post("/api/login", response_model=models.LoginSuccess)
def register(login: models.Login):
    if login.password:
        return models.LoginSuccess(token=secrets.token_hex(32))
    raise HTTPException(status_code=400, detail="Missing password")
