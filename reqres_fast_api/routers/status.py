from fastapi import APIRouter
from http import HTTPStatus

from reqres_fast_api.models.AppStatus import AppStatus
from reqres_fast_api.users_load import users

router = APIRouter(prefix="/api/status")


@router.get("/", status_code=HTTPStatus.OK)
async def status() -> AppStatus:
    return AppStatus(users=bool(users))


